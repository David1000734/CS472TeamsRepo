package nl.tudelft.jpacman.level;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;

import nl.tudelft.jpacman.npc.ghost.GhostFactory;
import nl.tudelft.jpacman.npc.Ghost;

import nl.tudelft.jpacman.points.PointCalculator;

import nl.tudelft.jpacman.sprite.PacManSprites;
import org.junit.jupiter.api.Test;

public class PvGCollisionsTest {

    @Test
    void playerAgainstGhost(){
        // Creates a player object
        // Given from Task 2 / PlayerTest.java
        PacManSprites pacSprites = new PacManSprites();
        PlayerFactory plFactory = new PlayerFactory(pacSprites);
        Player pl = plFactory.createPacMan();

        // Creates a Ghost via a GhostFactory
        GhostFactory ghFactory = new GhostFactory(pacSprites);
        Ghost gh = ghFactory.createBlinky();

        // Creates a PlayerCollision Object by creating a fake
        // PointCalculator and then mimics a collision between
        // the generated ghost and player
        PointCalculator calc = mock(PointCalculator.class);
        PlayerCollisions plCollide = new PlayerCollisions(calc);
        plCollide.collide(pl, gh);

        // Checks that the player was set to die
        // and that the killer is our ghost
        assertThat(pl.isAlive()).isEqualTo(false);
        assertThat(pl.getKiller()).isEqualTo(gh);
    }
}
