// Copyright (c) Microsoft. All rights reserved.

import { Conversations } from './ChatState'; // Ensure correct imports

export interface ConversationsState {
    conversations: Conversations;
    selectedId?: string; // selectedId should be optional
    loggedInUserId?: string; // loggedInUserId should be optional
}

// Ensure that the ChatState import is correct and that the ChatState type is properly defined in './ChatState'

export const initialState: ConversationsState = {
    conversations: {
        // Initialize conversations properly
        // Add necessary properties and initial values here
    },
    selectedId: undefined,
    loggedInUserId: undefined,
};

