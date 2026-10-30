import { runAgent } from "./agent.ts";
console.log(
  await runAgent(process.argv.slice(2).join(" ") || "What time is it in UTC?"),
);
