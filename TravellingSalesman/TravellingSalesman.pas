program TravellingSalesman;

{$Mode ObjFpc}

uses
    cThreads, SysUtils, math, UniversalImage;

type
    TPoint = record
        x : Double;
        y : Double;
    end;

    TEdge = record
        CriticalSection : TRTLCriticalSection;        
        PointA : Integer;
        PointB : Integer;
        distance : Double;
    end;

const
    MaxIterations = 1000;
    IterationsPerTemp = 20000;
    
var
    Points : array of TPoint;
    Edges : array of TEdge;
    PointCount : Integer;
    RemainingsIterations : Int64;

procedure Exchange(maxIt : Integer; t : Double);
var
    a, b, it, temp : Integer;
    newDistanceA, newDistanceB : Double;
begin
    it := 0;
    while (it < maxIt) do
    begin                
        a := Random(PointCount);
        b := Random(PointCount);  
        
        if LongBool(TryEnterCriticalsection(Edges[a].CriticalSection)) then
        begin
            if LongBool(TryEnterCriticalsection(Edges[b].CriticalSection)) then
            begin
                if (Edges[a].PointA <> Edges[b].PointA) and (Edges[a].PointB <> Edges[b].PointB) and (Edges[a].PointA <> Edges[b].PointB) and (Edges[a].PointB <> Edges[b].PointA) then
                begin
                    Inc(it);              
                    
                    newDistanceA := hypot(Points[Edges[a].PointA].x-Points[Edges[b].PointB].x, Points[Edges[a].PointA].y-Points[Edges[b].PointB].y);
                    newDistanceB := hypot(Points[Edges[b].PointA].x-Points[Edges[a].PointB].x, Points[Edges[b].PointA].y-Points[Edges[a].PointB].y);
                
                    if (newDistanceA + newDistanceB < Edges[a].distance + Edges[b].distance) or (Random < exp(-((newDistanceA + newDistanceB) - (Edges[a].distance + Edges[b].distance))/t)) then
                    begin
                        temp := Edges[a].PointB;
                        Edges[a].PointB :=Edges[b].PointA;
                        Edges[b].PointA := temp;
                        Edges[a].distance := newDistanceA;
                        Edges[b].distance := newDistanceB;
                    end;             
                end;               
                LeaveCriticalSection(Edges[b].CriticalSection);
            end;
            LeaveCriticalSection(Edges[a].CriticalSection);
        end;
    end;
end;

function GetTemp : Double;
begin
    Exit(50*(RemainingsIterations/MaxIterations)**3);
end;

function CalculateThread(P : Pointer) : PtrInt;
begin
    while InterLockedDecrement64(RemainingsIterations) > 0 do
        Exchange(IterationsPerTemp, GetTemp);
    Exit(0);
end;

procedure SaveToImage(const FileName : AnsiString);
const
    Width = 1000;
    Height = 1000;
var
    Image : TUniversalImage;
    minX, maxX, minY, maxY : Double;
    i : Integer;

function ConvertCoordsX(d : Double) : Integer; inline;
begin
    Exit(Round((d-minX)/(maxX-minX)*Width));
end;

function ConvertCoordsY(d : Double) : Integer; inline;
begin
    Exit(Round((d-minY)/(maxY-minY)*Height));
end;

begin
    Image := TUniversalImage.Create(Width, Height);

    minX := Points[0].x;
    maxX := Points[0].x;
    minY := Points[0].y;
    maxY := Points[0].y;
    for i := 0 to PointCount-1 do
        with Points[i] do
        begin            
            if x < minX then minX := x;
            if x > maxX then maxX := x;
            if y < minY then minY := y;
            if y > maxY then maxY := y;
        end;

    for i := 0 to PointCount-1 do
        With Edges[i] do
            Image.Canvas.Line(ConvertCoordsX(Points[PointA].x), ConvertCoordsY(Points[PointA].y), ConvertCoordsX(Points[PointB].x), ConvertCoordsY(Points[PointB].y));           

    Image.SaveToFile(FileName);
    Image.Free;
end;

var
    i  : Integer;
    TotalDistance : Double;
    
begin
    read(PointCount);
    Points := [];
    Edges := [];
    SetLength(Points, PointCount);
    SetLength(Edges, PointCount);    
    for i := 0 to PointCount-1 do
    begin
        InitCriticalSection(Edges[i].CriticalSection);
        Edges[i].PointA := i-1;
        Edges[i].PointB := i;
    end;
    Edges[0].PointA := PointCount-1;
        
    for i := 0 to PointCount-1 do
        read(Points[i].x, Points[i].y);

    for i := 0 to PointCount-1 do
        Edges[i].distance := hypot(Points[Edges[i].PointA].x-Points[Edges[i].PointB].x, Points[Edges[i].PointA].y-Points[Edges[i].PointB].y);

    
    RemainingsIterations := MaxIterations;

    //for i := 0 to 7 do
        BeginThread(@CalculateThread);
    
    repeat
        TotalDistance := 0;
        for i := 0 to PointCount-1 do
            TotalDistance += Edges[i].distance; 
        Writeln(RemainingsIterations, #9, GetTemp:4:4, #9, TotalDistance:4:4);
        sleep(1000);
    until RemainingsIterations <= 0;

    SaveToImage('Result.png');
    
    sleep(100);
    
    for i := 0 to PointCount-1 do
        DoneCriticalSection(Edges[i].CriticalSection);
    
end.

