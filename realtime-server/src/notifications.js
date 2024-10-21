/**
 * This module contains classes representing notification messages sent from the server to the client.
 * Each class contains a unique `code` that identifies the type of message on the client side.
 */


export class ComponentGeneratedCommunicate {
    /**
     * Message representing a response from the AI to a regeneration/update request.
     * Sent to the specific client that made the request.
     * 
     */
    code = 0;

    constructor(componentId, value) {
        this.component = componentId;
        this.value = value;
    }
}


export class ComponentCreatedCommunicate {
    /**
     * Notification sent when the AI completes the generation of a component for the first time.
     * Sent to all project members.
     */
    code = 1;

    constructor(componentId) {
        this.component = componentId;
    }
}


export class RegisterEditSessionCommunicate {
    /**
     * Notification informing about the start of a new editing session.
     * Sent to all project members.
     */
    code = 2;
    
    constructor(componentId, userId) {
        this.component = componentId;
        this.userId = userId;
    }
}


export class UnregisterEditSessionCommunicate {
    /**
     * Notification informing about the end of an editing session.
     * Sent to all project members.
     */
    code = 3;

    constructor(componentId) {
        this.component = componentId;
    }
}


export class ConfirmationRegisterEditionSessionCommunicate {
    /**
     * Notification informing about the successful registration of an editing session.
     * Sent to the client that requested the editing session.
     */
    code = 4;
}


export class ConfirmationUnregisterEditionSessionCommunicate {
    /**
     * Notification informing about the successful unregistration of an editing session.
     * Sent to the client that requested the editing session.
     */
    code = 5;
}


export class RejectedEditionSessionRegisterRequestCommunicate {
    /**
     * Notification informing about the rejection registration of an editing session.
     * Sent to the client that requested the editing session.
     */
    code = 6;

    constructor(details) {
        this.details = details;
    }
}


export class RejectedUpdateRequestCommunicate {
    /**
     * Notification informing about the rejection of an update request.
     * Sent to the client that made the request.
     */
    code = 7;

    constructor(details) {
        this.details = details;
    }
}


export class ConfirmedUpdateRequestCommunicate {
    /**
     * Notification informing about the confirmation of an update request.
     * Sent to the client that made the request.
     */
    code = 8;
}


export class DiscussionChatNoOlderMessagesCommunicate {
    /**
     * Notification informing that there are no more new messages in the discussion chat.
     * Sent to the client to indicate that all messages have been read.
     */
    code = 9;
}


export class AIChatNoOlderMessagesCommunicate {
    /**
     * Notification informing that there are no more new messages in the AI chat.
     * Sent to the client to indicate that all messages have been read.
     */
    code = 10;
}


export class RefreshEditionSessionsCommunicate {
    /**
     * Notification sent after a client reconnects, informing which components are currently being edited by users.
     * The map contains components as keys and the respective users as values.
     * Sent to the client to refresh their view of the current editing sessions.
     */
    code = 11;

    constructor(componentsToUserMap) {
        this.componentsToUserMap = componentsToUserMap;
    }
}
