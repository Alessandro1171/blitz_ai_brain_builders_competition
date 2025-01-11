import { FC } from 'react';
import { GameMap } from '../../types/index.ts';
import { Constants } from '../PlayZone.tsx';
export declare const RoadMarkings: FC<{
    currentGameIndex: number;
    map: GameMap;
    constants: Constants;
    teamZones: Array<Array<number>>;
    teamColors: Array<string>;
}>;
