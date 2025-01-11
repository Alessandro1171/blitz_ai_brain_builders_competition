export declare const ROAD: "EMPTY";
export declare const OBSTACLE: "WALL";
export declare const enum Roads {
    VerticalDoubleLeft = "RVerticalDoubleLeft",// 2 tile, broken line between
    VerticalDoubleRight = "RVerticalDoubleRight",// 2 tile, broken line between
    HorizontalDoubleTop = "RHorizontalDoubleTop",// 2 tile, broken line between
    HorizontalDoubleBottom = "RHorizontalBottom",// 2 tile, broken line between
    Cross = "RCross"
}
export type MapOverride = Array<Array<Roads | null>>;
export type MapRoadSides = Array<Array<number | null>>;
export declare enum RoadSide {
    Top = 8,
    Right = 4,
    Bottom = 2,
    Left = 1
}
