// Minimal MCP server with namespaced tools and concise/detailed responses.
// Replace with a real MCP SDK later.

type ResponseFormat = "concise" | "detailed";

export async function aws_ecs_plan(args: { service: string; image: string; response_format?: ResponseFormat }) {
  const { service, image, response_format = "concise" } = args;
  const plan = { service, image, checks: ["health-ok"], ids: { cluster: "...", taskdef: "..." } };
  if (response_format === "concise") {
    return {
      summary: `Update ${service} to ${image}. Health checks OK.`,
      next_steps: ["call aws.ecs_apply with plan_id"]
    };
  }
  return {
    summary: `Update ${service} to ${image}`,
    next_steps: ["call aws.ecs_apply with plan_id"],
    ids: plan.ids,
    plan
  };
}