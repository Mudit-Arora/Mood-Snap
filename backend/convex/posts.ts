import { internal } from "./_generated/api";
import { query, mutation, httpAction } from "./_generated/server";
import { v } from "convex/values";

export const list = mutation({
    handler: async (ctx) => {
        return await ctx.db.query('posts').order("desc").collect();
    },
});

export const add = mutation({
    args: { content: v.string() },
    handler: async (ctx, { content }) => {
        await ctx.db.insert("posts", { content: content, userId: "a", mood: "a" });
    },
});

export const comment = mutation({
    args: { postId: v.id('posts'), content: v.string() },
    handler: async (ctx, { postId, content }) => {
        await ctx.db.patch(postId, { comments: [{ content: content, userId: 'aa' }] });
    },
});


export default query(async ({ db }, { paginationOpts }) => {
    const opts = paginationOpts as any;
    return await db.query("posts").order("desc").paginate(opts);
});