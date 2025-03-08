import { Plugin } from "@elizaos/core";

// Import our Twilio actions
// Use relative path with .js extension to match the compiled output
import { makePhoneCallAction } from "./actions/makePhoneCallAction.js";
import { setupTwilioServerAction } from "./actions/setupTwilioServerAction.js";

// The Twilio plugin definition
export const twilioPlugin: Plugin = {
  name: "twilio-plugin",
  description: "Plugin for Twilio integration to enable phone calls from your agent",
  actions: [
    makePhoneCallAction,
    setupTwilioServerAction,
  ],
  evaluators: [],
  providers: [],
};

export { makePhoneCallAction, setupTwilioServerAction }; 