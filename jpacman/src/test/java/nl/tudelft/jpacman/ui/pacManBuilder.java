package nl.tudelft.jpacman.ui;

import nl.tudelft.jpacman.board.*;
import nl.tudelft.jpacman.game.Game;
import nl.tudelft.jpacman.game.GameFactory;
import nl.tudelft.jpacman.level.LevelFactory;
import nl.tudelft.jpacman.level.Level;
import nl.tudelft.jpacman.level.PlayerFactory;
import nl.tudelft.jpacman.npc.Ghost;
import nl.tudelft.jpacman.npc.ghost.GhostFactory;
import nl.tudelft.jpacman.points.PointCalculator;
import nl.tudelft.jpacman.sprite.PacManSprites;
import nl.tudelft.jpacman.sprite.Sprite;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;


class SimpleSquare extends Square {

    /**
     * Creates a new simple square.
     * Sourced from BasicSquare.java
     */
    SimpleSquare() {
        super();
    }

    @Override
    public boolean isAccessibleTo(Unit unit) {
        return true;
    }

    @Override
    @SuppressWarnings("return.type.incompatible")
    public Sprite getSprite() {
        return null;
    }
}

public class pacManBuilder {

    @Test
    void buildAPacMan(){
        // Pre-requisites to create the Level Factory and Game Factory
        PacManSprites pacSprites = new PacManSprites();
        PlayerFactory plFactory = new PlayerFactory(pacSprites);
        GhostFactory ghFactory = new GhostFactory(pacSprites);
        PointCalculator calc = mock(PointCalculator.class);
        LevelFactory levelCreator = new LevelFactory(pacSprites, ghFactory, calc);

        // Pre-requisites to making the Level with the LevelFactory
        // Most of this is sourced from SquareTest.java
        Square s1 = new SimpleSquare();
        BoardFactory boxMaker = new BoardFactory(pacSprites);
        Board box = boxMaker.createBoard(new Square[][]{{s1}});

        // Couple of blank lists to make the level
        List<Ghost> ghosts = new ArrayList<>();
        List<Square> startPositions = new ArrayList<>();

        // Adds a square as a starting position
        startPositions.add(s1);

        // Creates a level
        Level map = levelCreator.createLevel(box, ghosts, startPositions);

        // Makes a game object
        GameFactory gameMaker = new GameFactory(plFactory);
        Game isGame = gameMaker.createSinglePlayerGame(map, calc);

        // Uses game object to make the UI
        PacManUiBuilder pacManMaker = new PacManUiBuilder();
        PacManUI pac = null;
        pac = pacManMaker.build(isGame);

        // Tests that something was made
        assertThat(pac).isNotNull();
    }
}
