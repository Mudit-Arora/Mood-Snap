import { internal } from "./_generated/api";
import { query, mutation, httpAction } from "./_generated/server";
import { v } from "convex/values";

export const send = mutation({
    args: { body: v.string(), author: v.string() },
    handler: async (ctx, { body, author }) => {
        // Send a new message.
        await ctx.db.insert("messages", { body, author });
    },
});