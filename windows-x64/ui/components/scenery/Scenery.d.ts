import { FC } from 'react';
import { GameMap, Tick } from '../../types/index.ts';
import { Constants } from '../PlayZone.tsx';
export declare const Scenery: FC<{
    map: GameMap;
    tick: Tick;
    constants: Constants;
    teamZones: Array<Array<number>>;
    teamColors: Array<string>;
}>;
