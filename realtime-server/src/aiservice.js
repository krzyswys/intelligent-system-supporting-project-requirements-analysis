import { sendMessageByAI } from "./chat.js";
import { ComponentCreatedCommunicate } from "./notifications.js";
import { getComponentyByName } from "./model.js";


/**
 * AIService class handles communication and notifications for AI-related events.
 * It sends chat messages and notifies users when components are created.
 * 
 * @class AIService
*/
export class AIService {
    
    constructor(editionRegister, io, db) {
        this.editionRegister = editionRegister;
        this.io = io;
        this.db = db;
    }


    sendMessageOnChat(message) {
        /**
         * Sends a chat message through the AI service.
         * @param {Object} message - Object received from server.
        */
        sendMessageByAI(this.io, this.db, message.callback, message.content);
    }

    
    notifyComponentCreated(message) {
        /**
         * Notifies users when a component is created.
         * @param {Object} message - Object received from server.
        */
        const component = getComponentyByName(message?.component)

        this.io.to(message?.callback).emit(
            'notify-generation-complete', 
            new ComponentCreatedCommunicate(component?.id)
        );
    }
}
