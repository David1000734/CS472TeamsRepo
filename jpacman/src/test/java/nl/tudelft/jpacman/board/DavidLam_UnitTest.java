package nl.tudelft.jpacman.level;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import nl.tudelft.jpacman.sprite.PacManSprites;
import org.junit.jupiter.api.Test;
import nl.tudelft.jpacman.game.Game;
import nl.tudelft.jpacman.game.GameFactory;
import nl.tudelft.jpacman.game.SinglePlayerGame;
import nl.tudelft.jpacman.board.Board;
import nl.tudelft.jpacman.board.Square;
import nl.tudelft.jpacman.npc.Ghost;
import com.google.common.collect.Lists;

import nl.tudelft.jpacman.points.PointCalculator;
import nl.tudelft.jpacman.points.PointCalculatorLoader;

import static org.assertj.core.api.Assertions.assertThat;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class DavidLam_UnitTest {

    private static final PacManSprites SPRITE_STORE = new PacManSprites();
    private final PlayerFactory Factory = new PlayerFactory(SPRITE_STORE);
    private final Player player = Factory.createPacMan();

    private final GameFactory gameFactory = new GameFactory(Factory);

//    private Game SP_Game;

    /**
     * The level under test.
     */
    private Level level;

    /**
     * An NPC on this level.
     */
    private final Ghost ghost = mock(Ghost.class);

    /**
     * Starting position 1.
     */
    private final Square square1 = mock(Square.class);

    /**
     * Starting position 2.
     */
    private final Square square2 = mock(Square.class);

    /**
     * The board for this level.
     */
    private final Board board = mock(Board.class);

    /**
     * The collision map.
     */
    private final CollisionMap collisions = mock(CollisionMap.class);

    @Test
    void testAlive() {
        assertThat(player.isAlive()).isEqualTo(true);
    }

    @Test
    void testSetAlive() {
        player.setAlive(true);
        assertThat(player.isAlive()).isEqualTo(true);

        player.setAlive(false);
        assertThat(player.isAlive()).isEqualTo(false);
    }

    @Test
    void testScore() {
        // Upon initilization, score should be 0
        assertThat(player.getScore()).isEqualTo(0);
    }

    @Test
    void testSetScore() {
        int points = player.getScore();
        player.addPoints(1);

        assertThat(player.getScore()).isEqualTo(points + 1);
    }

    @Test
    void testStart() {
        final long defaultInterval = 100L;
        level = new Level(board, Lists.newArrayList(ghost), Lists.newArrayList(
            square1, square2), collisions);
        when(ghost.getInterval()).thenReturn(defaultInterval);

        level.start();

        assertThat(level.isInProgress()).isEqualTo(true);
        // Should also check to ensure every npc has an active ScheduledExecutorService
    }

    @Test
    void testStop() {
        final long defaultInterval = 100L;
        level = new Level(board, Lists.newArrayList(ghost), Lists.newArrayList(
            square1, square2), collisions);
        when(ghost.getInterval()).thenReturn(defaultInterval);

        level.stop();

        assertThat(level.isInProgress()).isEqualTo(false);
        // A better approach would be to also check that the npc hashmap does not
        // have any active ScheduledExecutorService
    }

    @Test
    void testAnyPlayerAlive() {
        final long defaultInterval = 100L;
        level = new Level(board, Lists.newArrayList(ghost), Lists.newArrayList(
            square1, square2), collisions);
        when(ghost.getInterval()).thenReturn(defaultInterval);

        // Didn't register players yet so should be false
        assertThat(level.isAnyPlayerAlive()).isEqualTo(false);

        // Register player
        level.registerPlayer(mock(Player.class));
    }
}
