package nl.tudelft.jpacman.level;

import nl.tudelft.jpacman.npc.ghost.GhostFactory;
import nl.tudelft.jpacman.points.DefaultPointCalculator;
import nl.tudelft.jpacman.points.PointCalculator;
import nl.tudelft.jpacman.sprite.PacManSprites;
import nl.tudelft.jpacman.sprite.Sprite;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class EdericOytas_UnitTest {

    private static final PacManSprites SPRITES = new PacManSprites();
    @Test
    void testIsAlive() {
        PlayerFactory factory = new PlayerFactory(SPRITES);
        Player player = factory.createPacMan();
        assertTrue(player.isAlive());
    }

    @Test
    void testPelletGetValue() {
        Sprite pellet_sprite = SPRITES.getPelletSprite();
        Pellet pellet = new Pellet(15, pellet_sprite);
        assertThat(pellet.getValue()).isEqualTo(15);
    }

    @Test
    void testPelletGetSprite() {
        Sprite pellet_sprite = SPRITES.getPelletSprite();
        Pellet pellet = new Pellet(15, pellet_sprite);
        assertThat(pellet.getSprite()).isEqualTo(pellet_sprite);
    }

    @Test
    void testLevelFactoryCreatePellet() {

        GhostFactory ghostFactory = new GhostFactory(SPRITES);
        PointCalculator pointCalculator = new DefaultPointCalculator();
        LevelFactory levelFactory = new LevelFactory(
            SPRITES, ghostFactory, pointCalculator
        );

        Sprite pelletSprite = SPRITES.getPelletSprite();
        Pellet pellet1 = levelFactory.createPellet();
        Pellet pellet2 = levelFactory.createPellet();

        assertThat(pellet1.getValue()).isEqualTo(10);
        assertThat(pellet2.getValue()).isEqualTo(10);
        assertThat(pellet1.getSprite()).isEqualTo(pelletSprite);
        assertThat(pellet2.getSprite()).isEqualTo(pelletSprite);

    }


}
