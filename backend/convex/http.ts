import { httpRouter } from "convex/server";
import { getPosts } from "./actions";

const http = httpRouter();

http.route({
    path: "/getPosts",
    method: "GET",
    handler: getPosts,
});

// Convex expects the router to be the default export of `convex/http.js`.
export default http;