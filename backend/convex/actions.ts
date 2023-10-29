import { api } from "./_generated/api";
import { httpAction } from "./_generated/server";

export const getPosts = httpAction(async (ctx, request) => {
    const posts = await ctx.runMutation(api.posts.list);

    const resp2 = new Response(JSON.stringify(posts), {
        status: 200,
    });

    return resp2;
});