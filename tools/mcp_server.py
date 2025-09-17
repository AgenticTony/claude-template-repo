# Minimal MCP server with namespaced tools and concise/detailed responses.
# Replace with a real MCP SDK later.

from typing import Literal, Dict, Any

def aws_ecs_plan(service: str, image: str, response_format: Literal["concise","detailed"]="concise") -> Dict[str, Any]:
    plan = {"service": service, "image": image, "checks": ["health-ok"], "ids": {"cluster":"...", "taskdef":"..."}}
    if response_format == "concise":
        return {
            "summary": f"Update {service} to {image}. Health checks OK.",
            "next_steps": ["call aws.ecs_apply with plan_id"]
        }
    return {
        "summary": f"Update {service} to {image}",
        "next_steps": ["call aws.ecs_apply with plan_id"],
        "ids": plan["ids"],
        "plan": plan
    }