// MongoDB 初始化脚本
db = db.getSiblingDB('agentpedia');

// 创建用户
db.createUser({
  user: 'agentpedia',
  pwd: 'agentpedia123',
  roles: [
    {
      role: 'readWrite',
      db: 'agentpedia'
    }
  ]
});

// 创建基础集合和索引
db.createCollection('agents');
db.createCollection('favorites');

// 创建索引
db.agents.createIndex({ "slug": 1 }, { unique: true });
db.agents.createIndex({ "status": 1 });
db.agents.createIndex({ "created_at": -1 });
db.agents.createIndex({
  "name.zh": "text",
  "name.en": "text",
  "description.short.zh": "text",
  "description.short.en": "text",
  "tags": "text"
}, {
  weights: {
    "name.zh": 10,
    "name.en": 10,
    "description.short.zh": 5,
    "description.short.en": 5,
    "tags": 8
  }
});

db.favorites.createIndex({ "user_id": 1 });
db.favorites.createIndex({ "agent_id": 1 });
db.favorites.createIndex({ "user_id": 1, "agent_id": 1 }, { unique: true });

print('MongoDB initialization completed');