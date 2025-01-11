import { FC, PropsWithChildren } from 'react';
import { GameMap } from '../../types';
import { Constants } from '../PlayZone';
export declare const TileGrid: FC<PropsWithChildren<{
    children: React.ReactNode;
    constants: Constants;
    map: GameMap;
    teamZones: Array<Array<number>>;
    teamColors: Array<string>;
}>>;
