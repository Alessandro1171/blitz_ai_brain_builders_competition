export interface Size {
    width: number;
    height: number;
}
export interface Vector {
    x: number;
    y: number;
}
export interface GameConstants {
    world: Size;
}
export interface Item {
    position: Vector;
    type: string;
    value: number;
}
export type TeamStats = Record<string, number>;
export type TickStats = Record<string, TeamStats>;
export interface Tick {
    currentTickNumber: number;
    characters: Character[];
    corpses: Array<Vector>;
    constants: GameConstants;
    map: GameMap;
    mapName: string;
    items: Array<Item>;
    score: Map<string, number>;
    stats: TickStats;
    teamInfos: Array<TeamInfo>;
    teamZoneGridPerIndex: Array<Array<number>>;
}
export interface TeamInfo {
    id: string;
    name: string;
    index: number;
}
export interface GameMap {
    height: number;
    width: number;
    tiles: Array<Array<number>>;
}
export interface Character {
    alive: boolean;
    id: string;
    numberOfCarriedItems: number;
    carriedItems: Array<Item>;
    position: Vector;
    spawnCooldown: number;
    spawnPoint: Vector;
    teamId: string;
    direction: Vector | null;
    index: number;
    skinIndex: number;
}
export interface AdditionalProperties {
}
