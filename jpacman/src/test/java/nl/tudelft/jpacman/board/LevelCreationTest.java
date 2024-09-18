package nl.tudelft.jpacman.board;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;

import nl.tudelft.jpacman.npc.Ghost;
import nl.tudelft.jpacman.npc.ghost.GhostFactory;
import nl.tudelft.jpacman.points.PointCalculator;
import nl.tudelft.jpacman.sprite.PacManSprites;
import nl.tudelft.jpacman.level.LevelFactory;
import nl.tudelft.jpacman.level.Level;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

public class LevelCreationTest {

    @Test
    void createALevel(){
        // Pre-requisites to making the LevelFactory
        PacManSprites pacSprites = new PacManSprites();
        GhostFactory ghFactory = new GhostFactory(pacSprites);
        PointCalculator calc = mock(PointCalculator.class);

        LevelFactory levelCreator = new LevelFactory(pacSprites, ghFactory, calc);

        // Pre-requisites to making the Level with the LevelFactory
        // Most of this is sourced from SquareTest.java
        Square s1 = new BasicSquare();
        BoardFactory boxMaker = new BoardFactory(pacSprites);
        Board box = boxMaker.createBoard(new Square[][]{{s1}});

        // Couple of blank lists to make the level
        List<Ghost> ghosts = new ArrayList<>();
        List<Square> startPositions = new ArrayList<>();

        Level map = null;
        map = levelCreator.createLevel(box, ghosts, startPositions);

        // Tests - first ensures a level was even made
        assertThat(map).isNotNull();
        // Checks that the board is still the same as generated
        assertThat(map.getBoard()).isEqualTo(box);
        // Level shouldn't have started
        assertThat(map.isInProgress()).isEqualTo(false);
        // There are no players, so none should be alive
        assertThat(map.isAnyPlayerAlive()).isEqualTo(false);
    }
}
