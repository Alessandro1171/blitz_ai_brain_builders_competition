package codes.blitz.game.bot;

import codes.blitz.game.generated.*;
import codes.blitz.game.generated.Character;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Bot {
  Random random = new Random();

  public Bot() {
    System.out.println("Initializing your super duper mega bot.");
  }

  /*
   * Here is where the magic happens. I bet you can do better ;)
   */
  public List<Action> getActions(TeamGameState gameMessage) {
    List<Action> actions = new ArrayList<>();

    for (Character character : gameMessage.yourCharacters()) {
      List<Action> possibleActions =
          List.of(
              new MoveUpAction(character.id()),
              new MoveRightAction(character.id()),
              new MoveDownAction(character.id()),
              new MoveLeftAction(character.id()),
              new GrabAction(character.id()),
              new DropAction(character.id()));

      Action randomlyPickedAction = possibleActions.get(random.nextInt(possibleActions.size()));
      actions.add(randomlyPickedAction);
    }

    // You can clearly do better than the random actions above. Have fun!!
    return actions;
  }
}
