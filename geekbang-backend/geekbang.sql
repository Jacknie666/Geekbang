-- USERS 表
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  open_id VARCHAR(32) NOT NULL UNIQUE COMMENT '微信/OpenID',
  union_id VARCHAR(32) DEFAULT NULL COMMENT '微信/UnionID',
  nick_name VARCHAR(50) DEFAULT NULL COMMENT '昵称',
  password VARCHAR(255) DEFAULT NULL COMMENT '密码',
  avatar_url VARCHAR(255) DEFAULT NULL COMMENT '头像链接',
  is_verified TINYINT(1) DEFAULT 0 COMMENT '是否已学籍认证',
  verified_university VARCHAR(50) DEFAULT NULL COMMENT '认证的学校名称',
  description TEXT DEFAULT NULL COMMENT '用户描述',
  tag VARCHAR(50) DEFAULT NULL COMMENT '用户标签',
  credit_score INT DEFAULT 100 COMMENT '信用分',
  balance DECIMAL(10, 2) DEFAULT 0.00 COMMENT '账户余额',
  where_from VARCHAR(50) DEFAULT '1' COMMENT '用户来源：1小程序、2其他',
  status TINYINT DEFAULT 1 COMMENT '用户状态：1=正常，0=封禁，-1=注销',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX idx_union_id (union_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- POSTS 表
CREATE TABLE posts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL COMMENT '发布者ID（关联users.id）',
  post_id VARCHAR(32) NOT NULL COMMENT '帖子ID',
  content TEXT NOT NULL COMMENT '内容',
  likes_count INT DEFAULT 0 COMMENT '点赞数',
  comments_count INT DEFAULT 0 COMMENT '评论数',
  status TINYINT DEFAULT 1 COMMENT '状态：1=正常，0=隐藏，-1=删除',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at)
);


-- COMMENTS 表
CREATE TABLE comments (
  id INT PRIMARY KEY AUTO_INCREMENT,
  post_id INT NOT NULL COMMENT '帖子ID（关联posts.id）',
  user_id INT NOT NULL COMMENT '评论者ID（关联users.id）',
  comment_id INT DEFAULT NULL COMMENT '评论ID（用于回复评论）',
  parent_id INT DEFAULT NULL COMMENT '父评论ID（用于嵌套评论）',
  content TEXT NOT NULL COMMENT '评论内容',
  likes_count INT DEFAULT 0 COMMENT '点赞数',
  status TINYINT DEFAULT 1 COMMENT '状态：1=正常，-1=删除',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE SET NULL,
  INDEX idx_post_id (post_id),
  INDEX idx_user_id (user_id)
);


-- LIKES 表
CREATE TABLE likes (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL COMMENT '点赞用户ID',
  post_id INT DEFAULT NULL COMMENT '帖子ID',
  comment_id INT DEFAULT NULL COMMENT '评论ID',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
  FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
  UNIQUE KEY uniq_like (user_id, post_id, comment_id),
  INDEX idx_user_id (user_id),
  INDEX idx_post_id (post_id),
  INDEX idx_comment_id (comment_id)
);


-- RELATIONSHIPS 表
CREATE TABLE relationships (
  id INT PRIMARY KEY AUTO_INCREMENT,
  follower_id INT NOT NULL COMMENT '关注者ID',
  following_id INT NOT NULL COMMENT '被关注者ID',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  status TINYINT DEFAULT 1 COMMENT '状态：1=关注，0=取消关注',
  FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY uniq_follow (follower_id, following_id),
  INDEX idx_follower_id (follower_id),
  INDEX idx_following_id (following_id)
);


-- MESSAGES 表
CREATE TABLE messages (
  id INT PRIMARY KEY AUTO_INCREMENT,
  message_id VARCHAR(32) NOT NULL UNIQUE COMMENT '消息ID',
  conversation_id VARCHAR(32) NOT NULL COMMENT '对话ID',
  sender_id INT NOT NULL COMMENT '发送者ID',
  receiver_id INT NOT NULL COMMENT '接收者ID',
  content TEXT NOT NULL COMMENT '消息内容',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_sender_receiver (sender_id, receiver_id),
  INDEX idx_receiver_created (receiver_id, created_at)
);


-- CONVERSATIONS 表
CREATE TABLE conversations (
  id INT PRIMARY KEY AUTO_INCREMENT,
  conversation_id VARCHAR(32) NOT NULL COMMENT '对话ID',
  user_id INT NOT NULL COMMENT '用户ID',
  target_id INT NOT NULL COMMENT '对话目标ID（用户或群组）',
  last_message_id VARCHAR(32) DEFAULT NULL COMMENT '最后一条消息ID',
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (last_message_id) REFERENCES messages(message_id) ON DELETE SET NULL,
  UNIQUE KEY uniq_user_target (user_id, target_id),
  INDEX idx_user_updated (user_id, updated_at)
);
