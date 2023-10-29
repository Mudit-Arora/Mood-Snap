import { defineSchema, defineTable } from "convex/server";
import { Validator, v } from "convex/values";

export default defineSchema({
    posts: defineTable({
        content: v.string(),
        userId: v.string(),
        mood: v.optional(v.string()),
        comments: v.optional(v.array(
            v.object({
                content: v.string(),
                userId: v.string(),
            }),
        )),
    }),
});