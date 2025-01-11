import { FC } from 'react';
import { type Character, type TeamInfo } from '../../types';
import { Constants } from '../PlayZone';
interface SpawnPointProps {
    character: Character;
    constants: Constants;
    teamInfos: Array<TeamInfo>;
    teamColors: Array<string>;
}
export declare const SpawnPoint: FC<SpawnPointProps>;
export {};
