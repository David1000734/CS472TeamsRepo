package nl.tudelft.jpacman.points;

import nl.tudelft.jpacman.board.Direction;
import nl.tudelft.jpacman.level.LevelFactory;
import nl.tudelft.jpacman.level.Pellet;
import nl.tudelft.jpacman.level.Player;
import nl.tudelft.jpacman.level.PlayerFactory;
import nl.tudelft.jpacman.npc.Ghost;
import nl.tudelft.jpacman.npc.ghost.GhostFactory;
import nl.tudelft.jpacman.sprite.PacManSprites;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class JoshRichardsonTest {

    // create pacman
    private final PacManSprites mySprites = new PacManSprites();
    private final PlayerFactory myPlayerFactory = new PlayerFactory(mySprites);
    private final Player myPacMan = myPlayerFactory.createPacMan();

    // create pellet
    private final GhostFactory myGhostFactory = new GhostFactory(mySprites);
    private final DefaultPointCalculator myCalculator = new DefaultPointCalculator();
    private final LevelFactory myLevelFactory = new LevelFactory(mySprites, myGhostFactory, myCalculator);
    private final Pellet myPellet = myLevelFactory.createPellet();

    // create ghost
    private final Ghost pinky = myGhostFactory.createPinky();

    // create one of each direction
    private final Direction myDirection1 = Direction.valueOf("NORTH");
    private final Direction myDirection2 = Direction.valueOf("SOUTH");
    private final Direction myDirection3 = Direction.valueOf("EAST");
    private final Direction myDirection4 = Direction.valueOf("WEST");

    // let player starts with 0 points
    // then they should not gain points for colliding with ghost
    @Test
    void testCollidedWithGhost(){
        myCalculator.collidedWithAGhost(myPacMan, pinky);
        assertThat(myPacMan.getScore()).isEqualTo(0);
    }

    // let player start with 0 points
    // if they consume a pellet then their score should equal the pellets value
    @Test
    void testConsumedPellet(){
        myCalculator.consumedAPellet(myPacMan, myPellet);
        assertThat(myPacMan.getScore()).isEqualTo(myPellet.getValue());
    }

    // let player start with 0 points
    // if the player moves in any direction then they should not gain points
    @Test
    void testPacManMoved(){
        myCalculator.pacmanMoved(myPacMan, myDirection1);
        myCalculator.pacmanMoved(myPacMan, myDirection2);
        myCalculator.pacmanMoved(myPacMan, myDirection3);
        myCalculator.pacmanMoved(myPacMan, myDirection4);
        assertThat(myPacMan.getScore()).isEqualTo(0);
    }
}
