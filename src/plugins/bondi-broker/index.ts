import { Plugin } from "@elizaos/core";
import { createWalletAction } from "./actions/createWallet.ts";
import { investAction } from "./actions/invest.ts";
import { checkInvestmentAction } from "./actions/checkInvestment.ts";
import { fundingInformationAction } from "./actions/fundingInformation.ts";

// Import Twilio actions
import { makePhoneCallAction } from "../../plugins/twilio/actions/makePhoneCallAction.js";
import { setupTwilioServerAction } from "../../plugins/twilio/actions/setupTwilioServerAction.js";

/**
 * Bondi broker plugin for Eliza
 * @module bondiBrokerPlugin
 */
export const bondiBrokerPlugin: Plugin = {
  name: "bondi-broker-plugin",
  description: "Bondi Finance broker plugin for investment and wallet actions",
  actions: [
    createWalletAction,
    investAction,
    checkInvestmentAction,
    fundingInformationAction,
    makePhoneCallAction,
    setupTwilioServerAction
  ],
  evaluators: [],
  providers: [],
};

export { createWalletAction, investAction, makePhoneCallAction, setupTwilioServerAction };

export default bondiBrokerPlugin; 