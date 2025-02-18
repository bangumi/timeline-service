import html
import time
from typing import Optional

import php_serialize
import pydantic
from grpc import RpcContext
from sqlalchemy.orm import Session
from sslog import logger

from api.v1 import timeline_pb2_grpc
from api.v1.timeline_pb2 import (
    EpisodeCollectRequest,
    EpisodeCollectResponse,
    HelloRequest,
    HelloResponse,
    SubjectCollectRequest,
    SubjectCollectResponse,
    SubjectProgressRequest,
    SubjectProgressResponse,
)
from chii.config import config
from chii.db import sa
from chii.db.tables import (
    ChiiTimeline,
    ChiiTimeline_column_id,
    ChiiTimeline_column_uid,
)
from chii.timeline import (
    SUBJECT_TYPE_MAP,
    ProgressMemo,
    SubjectMemo,
    TimelineCat,
    TimelineSource,
)

BatchMeme: pydantic.TypeAdapter[dict[int, SubjectMemo]] = pydantic.TypeAdapter(
    dict[int, SubjectMemo]
)


class TimeLineService(timeline_pb2_grpc.TimeLineServiceServicer):
    def __init__(self):
        self.SessionMaker = sa.sync_session_maker()

    def Hello(self, request: HelloRequest, context) -> HelloResponse:
        return HelloResponse(message=f"hello from {request.name}")

    def SubjectCollect(
        self, req: SubjectCollectRequest, context: RpcContext
    ) -> SubjectCollectResponse:
        """
        cat 3 看过/读过/抛弃了...

        https://github.com/bangumi/dev-docs/blob/master/Timeline.md#cat_sbj_collect-条目收藏
        """
        if config.debug:
            logger.debug("request {!r}", req)

        try:
            return self.__subject_collect(req)
        except:
            logger.exception("exception in SubjectCollect")
            raise

    def __subject_collect(self, req: SubjectCollectRequest) -> SubjectCollectResponse:
        tlType = SUBJECT_TYPE_MAP[req.subject.type][req.collection]
        logger.debug("request: {!r}", req)
        with self.SessionMaker.begin() as session:
            tl: Optional[ChiiTimeline] = (
                session.query(ChiiTimeline)
                .where(ChiiTimeline_column_uid == req.user_id)
                .order_by(ChiiTimeline_column_id.desc())
                .limit(1)
                .scalar()
            )

            if tl and tl.created_at >= int(time.time() - 10 * 60):
                logger.info("find previous timeline, merging")
                if tl.cat == TimelineCat.Subject and tl.type == tlType:
                    self.merge_previous_timeline(session, tl, req)
                    return SubjectCollectResponse(ok=True)

            logger.info(
                "missing previous timeline or timeline type mismatch, create a new timeline"
            )
            self.create_subject_collection_timeline(session, req, tlType)
            session.commit()

        return SubjectCollectResponse(ok=True)

    @staticmethod
    def merge_previous_timeline(
        session: Session, tl: ChiiTimeline, req: SubjectCollectRequest
    ):
        escaped = html.escape(req.comment)
        if tl.batch:
            memo = BatchMeme.validate_python(php_serialize.loads(tl.memo))
        else:
            m = SubjectMemo.model_validate(php_serialize.loads(tl.memo))
            if int(m.subject_id) == req.subject.id:
                # save request called twice, just ignore
                should_update = False
                if m.collect_comment != escaped:
                    should_update = True
                    m.collect_comment = escaped

                if m.collect_rate != req.rate:
                    should_update = True
                    m.collect_rate = req.rate

                if should_update:
                    tl.memo = php_serialize.dumps(m.model_dump()).decode()
                    session.add(tl)
                return

            memo = {int(m.subject_id): m}

        memo[req.subject.id] = SubjectMemo(
            subject_id=str(req.subject.id),
            collect_comment=escaped,
            collect_rate=req.rate,
            collect_id=req.collection_id,
        )

        tl.batch = 1
        tl.memo = php_serialize.dumps(
            {key: value.model_dump() for key, value in memo.items()}
        ).decode()

        session.add(tl)

    @staticmethod
    def create_subject_collection_timeline(
        session: Session, req: SubjectCollectRequest, type: int
    ):
        memo = SubjectMemo(
            subject_id=str(req.subject.id),
            collect_comment=html.escape(req.comment),
            collect_rate=req.rate,
            collect_id=req.collection_id,
        )

        session.add(
            ChiiTimeline(
                cat=TimelineCat.Subject,
                type=type,
                uid=req.user_id,
                memo=php_serialize.dumps(memo.model_dump()).decode(),
                batch=0,
                related=str(req.subject.id),
                source=TimelineSource.api,
            )
        )

    def EpisodeCollect(
        self, req: EpisodeCollectRequest, context
    ) -> EpisodeCollectResponse:
        """
        cat 4 type 2 "看过 ep2 ${subject name}"
        """
        if config.debug:
            logger.debug("request {!r}", req)

        try:
            return self.__episode_collect(req)
        except:
            logger.exception("exception in EpisodeCollectRequest")
            raise

    def __episode_collect(self, req: EpisodeCollectRequest) -> EpisodeCollectResponse:
        """
        cat 4 type 2 "看过 ep2 ${subject name}"
        """
        tlType = 2
        memo = ProgressMemo(
            ep_id=req.last.id,
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
        )

        with self.SessionMaker.begin() as session:
            tl: Optional[ChiiTimeline] = (
                session.query(ChiiTimeline)
                .where(ChiiTimeline_column_uid == req.user_id)
                .order_by(ChiiTimeline_column_id.desc())
                .limit(1)
                .scalar()
            )

            if tl and tl.created_at >= int(time.time() - 15 * 60):
                logger.info("find previous timeline, updating", user_id=req.user_id)
                if (
                    tl.cat == TimelineCat.Progress
                    and tl.type == tlType
                    and tl.batch == 0
                    and tl.related == str(req.subject.id)
                ):
                    tl.memo = php_serialize.dumps(memo.model_dump()).decode()
                    tl.source = TimelineSource.api
                    session.add(tl)
                    return EpisodeCollectResponse(ok=True)

            session.add(
                ChiiTimeline(
                    uid=req.user_id,
                    memo=php_serialize.dumps(memo.model_dump()).decode(),
                    cat=TimelineCat.Progress,
                    type=tlType,
                    source=TimelineSource.api,
                    batch=0,
                    related=str(req.subject.id),
                )
            )
            session.commit()

        return EpisodeCollectResponse(ok=True)

    def SubjectProgress(
        self, req: SubjectProgressRequest, context
    ) -> SubjectProgressResponse:
        """
        cat 4 type 0
        """
        if config.debug:
            logger.debug("request {!r}", req)

        try:
            return self.__subject_progress(req)
        except:
            logger.exception("exception in SubjectProgress")
            raise

    def __subject_progress(
        self, req: SubjectProgressRequest
    ) -> SubjectProgressResponse:
        """
        cat 4 type 0
        """
        tlType = 0

        memo = ProgressMemo(
            subject_id=str(req.subject.id),
            subject_type_id=str(req.subject.type),
            eps_total=str(req.subject.eps_total) if req.subject.eps_total else "??",
            vols_total=str(req.subject.vols_total) if req.subject.vols_total else "??",
            eps_update=req.eps_update,
            vols_update=req.vols_update,
        )

        with self.SessionMaker.begin() as session:
            tl: Optional[ChiiTimeline] = (
                session.query(ChiiTimeline)
                .where(ChiiTimeline_column_uid == req.user_id)
                .order_by(ChiiTimeline_column_id.desc())
                .limit(1)
                .scalar()
            )

            if tl and tl.created_at >= int(time.time() - 15 * 60):
                logger.info("find previous timeline, updating", user_id=req.user_id)
                if (
                    tl.cat == TimelineCat.Progress
                    and tl.type == tlType
                    and tl.batch == 0
                    and tl.related == str(req.subject.id)
                ):
                    tl.memo = php_serialize.dumps(memo.model_dump()).decode()
                    tl.source = TimelineSource.api
                    session.add(tl)
                    session.commit()
                    return SubjectProgressResponse(ok=True)

            session.add(
                ChiiTimeline(
                    uid=req.user_id,
                    memo=php_serialize.dumps(memo.model_dump()).decode(),
                    cat=TimelineCat.Progress,
                    type=tlType,
                    batch=0,
                    related=str(req.subject.id),
                    source=TimelineSource.api,
                )
            )
            session.commit()

        return SubjectProgressResponse(ok=True)
