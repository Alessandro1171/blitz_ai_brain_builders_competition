namespace Application;

public class Bot
{
    public const string NAME = "My cool C# bot";
    private readonly Random _random = new Random();

    /// <summary>
    /// This method should be used to initialize some variables you will need throughout the game.
    /// </summary>
    public Bot()
    {
        Console.WriteLine("Initializing your super mega bot!");
    }

    /// <summary>
    /// Here is where the magic happens, for now the moves are random. I bet you can do better ;)
    /// </summary>
    public IEnumerable<Action> GetNextMoves(TeamGameState gameMessage)
    {
        var actions = new List<Action>();

        foreach (Character character in gameMessage.YourCharacters)
        {
            var possibleActions = new List<Action>
            {
                new MoveUpAction(character.Id),
                new MoveRightAction(character.Id),
                new MoveDownAction(character.Id),
                new MoveLeftAction(character.Id),
                new GrabAction(character.Id),
                new DropAction(character.Id),
            };

            var randomlyPickedAction = possibleActions[_random.Next(possibleActions.Count)];
            actions.Add(randomlyPickedAction);
        }

        // You can clearly do better than the random actions above. Have fun!!
        return actions;
    }
}
