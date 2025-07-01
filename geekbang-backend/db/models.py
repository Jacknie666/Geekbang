from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, DECIMAL, UniqueConstraint, Index, SmallInteger
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    open_id = Column(String(32), unique=True, nullable=False, comment='微信/OpenID')
    union_id = Column(String(32), nullable=True, comment='微信/UnionID')
    nick_name = Column(String(50), nullable=True, comment='昵称')
    password = Column(String(255), nullable=True, comment='密码')
    avatar_url = Column(String(255), nullable=True, comment='头像链接')
    is_verified = Column(SmallInteger, default=0, comment='是否已学籍认证')
    verified_university = Column(String(50), nullable=True, comment='认证的学校名称')
    description = Column(Text, nullable=True, comment='用户描述')
    tag = Column(String(50), nullable=True, comment='用户标签')
    credit_score = Column(Integer, default=100, comment='信用分')
    balance = Column(DECIMAL(10, 2), default=0.00, comment='账户余额')
    where_from = Column(String(50), default='1', comment='用户来源：1小程序、2其他')
    status = Column(SmallInteger, default=1, comment='用户状态：1=正常，0=封禁，-1=注销')
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', comment='创建时间')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP', comment='更新时间')

    __table_args__ = (
        Index('idx_union_id', 'union_id'),
    )

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='发布者ID')
    post_id = Column(String(32), nullable=False, comment='帖子ID')
    content = Column(Text, nullable=False, comment='内容')
    likes_count = Column(Integer, default=0, comment='点赞数')
    comments_count = Column(Integer, default=0, comment='评论数')
    status = Column(SmallInteger, default=1, comment='状态')
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_created_at', 'created_at'),
    )

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, comment='帖子ID')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='评论者ID')
    comment_id = Column(Integer, nullable=True, comment='评论ID')
    parent_id = Column(Integer, ForeignKey('comments.id', ondelete='SET NULL'), nullable=True, comment='父评论ID')
    content = Column(Text, nullable=False, comment='评论内容')
    likes_count = Column(Integer, default=0, comment='点赞数')
    status = Column(SmallInteger, default=1, comment='状态')
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')

    __table_args__ = (
        Index('idx_post_id', 'post_id'),
        Index('idx_user_id', 'user_id'),
    )

class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='点赞用户ID')
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=True, comment='帖子ID')
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'), nullable=True, comment='评论ID')
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', 'comment_id', name='uniq_like'),
        Index('idx_user_id', 'user_id'),
        Index('idx_post_id', 'post_id'),
        Index('idx_comment_id', 'comment_id'),
    )

class Relationship(Base):
    __tablename__ = 'relationships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='关注者ID')
    following_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='被关注者ID')
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    status = Column(SmallInteger, default=1, comment='状态')

    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='uniq_follow'),
        Index('idx_follower_id', 'follower_id'),
        Index('idx_following_id', 'following_id'),
    )

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(32), unique=True, nullable=False, comment='消息ID')
    conversation_id = Column(String(32), nullable=False, comment='对话ID')
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='发送者ID')
    receiver_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='接收者ID')
    content = Column(Text, nullable=False, comment='消息内容')
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')

    __table_args__ = (
        Index('idx_sender_receiver', 'sender_id', 'receiver_id'),
        Index('idx_receiver_created', 'receiver_id', 'created_at'),
    )

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(32), nullable=False, comment='对话ID')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    target_id = Column(Integer, nullable=False, comment='对话目标ID')
    last_message_id = Column(String(32), ForeignKey('messages.message_id', ondelete='SET NULL'), nullable=True, comment='最后一条消息ID')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')

    __table_args__ = (
        UniqueConstraint('user_id', 'target_id', name='uniq_user_target'),
        Index('idx_user_updated', 'user_id', 'updated_at'),
    )
