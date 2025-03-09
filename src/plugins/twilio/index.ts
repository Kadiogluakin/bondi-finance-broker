import { Plugin, Provider, IAgentRuntime, State, Memory } from "@elizaos/core";

// Import our Twilio actions
// Use relative path with .js extension to match the compiled output
import { makePhoneCallAction } from "./actions/makePhoneCallAction.js";
import { setupTwilioServerAction } from "./actions/setupTwilioServerAction.js";
import { TwilioConnector } from "./connector.js";
import { suggestCallEvaluator } from "./evaluators/suggestCallEvaluator.js";

// Map to store connector instances by runtime ID
const connectorMap = new Map<string, TwilioConnector>();

// Provider to synchronize memory between Twilio and Eliza
const twilioMemoryProvider: Provider = {
  // The Provider interface requires a 'get' method
  get: async (runtime: IAgentRuntime, message: Memory, state?: State) => {
    try {
      // Check if we need to initialize
      if (!connectorMap.has(runtime.agentId)) {
        const connector = new TwilioConnector(runtime);
        connectorMap.set(runtime.agentId, connector);
        
        // Start polling for voice interactions
        connector.startPolling();
        
        console.log(`Initialized Twilio memory provider for agent ${runtime.agentId}`);
      }
      
      // If we have a connector and userId, export chat memory for voice calls
      const connector = connectorMap.get(runtime.agentId);
      if (connector && state?.userId) {
        await connector.exportChatMemory(state.userId);
      }
      
      // Return an empty object since we're just handling the side effects
      return {};
    } catch (error) {
      console.error('Error in Twilio memory provider:', error);
      return {};
    }
  }
};

// The Twilio plugin definition
export const twilioPlugin: Plugin = {
  name: "twilio-plugin",
  description: "Plugin for Twilio integration to enable phone calls from your agent",
  actions: [
    makePhoneCallAction,
    setupTwilioServerAction,
  ],
  evaluators: [
    suggestCallEvaluator
  ],
  providers: [
    twilioMemoryProvider
  ],
};

export { makePhoneCallAction, setupTwilioServerAction, TwilioConnector, suggestCallEvaluator }; 