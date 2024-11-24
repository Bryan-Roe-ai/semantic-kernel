module SemanticKernel.Types

// Basic geometric types and calculations
type Point = { X: float; Y: float }

type Shape =
    | Circle of radius: float * center: Point
    | Rectangle of width: float * height: float * topLeft: Point
    | Triangle of p1: Point * p2: Point * p3: Point

// Validation functions
let createPoint x y = { X = x; Y = y }

let createCircle radius center : Result<Shape, string> =
    if radius <= 0.0 then
        Error "Radius must be positive"
    else
        Ok (Circle(radius, center))