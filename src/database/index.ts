import { PostgresDatabaseAdapter } from "@elizaos/adapter-postgres";
import { SqliteDatabaseAdapter } from "@elizaos/adapter-sqlite";
import Database from "better-sqlite3";
import path from "path";

// Create a simple in-memory database adapter that won't rely on SQLite bindings
class InMemoryDatabaseAdapter {
  private memories = new Map();
  private caches = new Map();
  
  async init() {
    console.log("Initialized in-memory database adapter");
    return true;
  }
  
  async createMemory(memory, tableName, unique = false) {
    const key = `${tableName}_${memory.id}`;
    this.memories.set(key, memory);
    return true;
  }
  
  async getMemories({ roomId, tableName, count = 10 }) {
    // Return empty array as we're just trying to get the agent running
    return [];
  }
  
  async searchMemories() {
    // Return empty array
    return [];
  }
  
  // Cache methods with signatures matching IDatabaseCacheAdapter
  async createCache(params: { agentId: string; key: string; value: string }) {
    const cacheKey = `${params.agentId}_${params.key}`;
    this.caches.set(cacheKey, params.value);
    return true;
  }
  
  async getCache(params: { agentId: string; key: string }) {
    const cacheKey = `${params.agentId}_${params.key}`;
    return this.caches.get(cacheKey) || null;
  }
  
  async setCache(params: { agentId: string; key: string; value: string }) {
    const cacheKey = `${params.agentId}_${params.key}`;
    this.caches.set(cacheKey, params.value);
    return true;
  }
  
  async deleteCache(params: { agentId: string; key: string }) {
    const cacheKey = `${params.agentId}_${params.key}`;
    this.caches.delete(cacheKey);
    return true;
  }
  
  // Add any other required methods with simple implementations
  async getRelationships() { return []; }
  async createRelationship() { return true; }
  async removeRelationship() { return true; }
}

export function initializeDatabase(dataDir: string) {
  try {
    if (process.env.POSTGRES_URL) {
      const db = new PostgresDatabaseAdapter({
        connectionString: process.env.POSTGRES_URL,
      });
      return db;
    } else {
      // Try SQLite with in-memory database
      try {
        const filePath = ":memory:";
        const db = new SqliteDatabaseAdapter(new Database(filePath));
        return db;
      } catch (sqliteError) {
        console.log("SQLite initialization failed, using in-memory adapter", sqliteError);
        // If SQLite fails, use our in-memory adapter
        return new InMemoryDatabaseAdapter();
      }
    }
  } catch (error) {
    console.log("Database initialization failed, using in-memory adapter", error);
    // Fallback to in-memory adapter if all else fails
    return new InMemoryDatabaseAdapter();
  }
}
