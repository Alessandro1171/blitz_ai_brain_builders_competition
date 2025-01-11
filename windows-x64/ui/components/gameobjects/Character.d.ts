import { FC } from 'react';
import { type Character, type TeamInfo } from '../../types';
import { Constants } from '../PlayZone';
interface CharacterSpriteProps {
    character: Character;
    constants: Constants;
    teamInfos: Array<TeamInfo>;
    teamZones: Array<Array<number>>;
    teamColors: Array<string>;
}
export declare const CharacterSprite: FC<CharacterSpriteProps>;
export {};
