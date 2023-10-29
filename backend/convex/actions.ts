import { api } from "./_generated/api";
import { httpAction } from "./_generated/server";

export const postMessage = httpAction(async (ctx, request) => {
    const { author, body } = await request.json();

    await ctx.runMutation(api.messages.send, {
        body: `Sent via HTTP action: ${body}`,
        author,
    });

    return new Response(null, {
        status: 200,
    });
});

export const getPosts = httpAction(async (ctx, request) => {
    const posts = await ctx.runMutation(api.posts.list);

    const resp2 = new Response(JSON.stringify(posts), {
        status: 200,
    });

    return resp2;
});