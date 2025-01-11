import { TeamGameState, Action, ActionType } from './GameInterface';

export class Bot {
    constructor() {
        console.log('Initializing your super duper mega bot');
        // This method should be used to initialize some variables you will need throughout the game.
    }

    /*
     * Here is where the magic happens, for now the moves are random. I bet you can do better ;)
     */
    getNextMoves(gameMessage: TeamGameState): Action[] {
        const errors = gameMessage.lastTickErrors;
        if (errors.length > 0) {
            console.error('Errors:', errors);
        }
        const actions: Action[] = [];

        for (const character of gameMessage.yourCharacters) {
            const possibleActions: Action[] = [
                { type: ActionType.MOVE_LEFT, characterId: character.id  },
                { type: ActionType.MOVE_RIGHT, characterId: character.id  },
                { type: ActionType.MOVE_UP, characterId: character.id  },
                { type: ActionType.MOVE_DOWN, characterId: character.id },
                { type: ActionType.GRAB, characterId: character.id },
                { type: ActionType.DROP, characterId: character.id },
            ];

            actions.push(randomlyChoose(possibleActions));
        }
        

        // You can clearly do better than the random actions above. Have fun!!
        return actions;
    }
}

function randomlyChoose<T>(arr: T[]): T {
    return arr[Math.floor(arr.length * Math.random())];
}
