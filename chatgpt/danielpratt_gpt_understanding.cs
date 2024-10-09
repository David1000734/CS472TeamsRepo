using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LemonGrenade : MonoBehaviour
{
    private Vector3 targetlocation; // Location of the target (player's position)
    PlayerHealth playerHealth;      // Reference to the player's health script
    GameObject player;              // Reference to the player object

    
    public float multiplier;        // Speed multiplier to scale the grenade's speed
    public float max, min;          // Maximum and minimum scaling limits for the grenade's size
    public float scalingFactor;     // Scaling factor for adjusting the grenade's size over time
    public float baseDamage;        // Base damage of the grenade  
    public float explosionRange;    // The explosion radius of the grenade


    protected float initialSpeed;       // Initial speed of the grenade based on distance
    protected float distance;           // Distance between grenade and target 
    protected float currentDistance;    // Current distance between grenade and target
    protected float curTime;            // Timer for how long the grenade has been active
    protected float speed;              // Speed of the grenade as it moves towards the player
    private float grenadeDamage;        // The amount of damage dealt by the grenade
    private float playerDistance;       // Distance between the grenade and the player



    // Initialization. Do this upon the grenade being thrown
    private void Start()
    {
        // Find the player object using its tag and get their health component
        player = GameObject.FindGameObjectWithTag("Player");
        playerHealth = player.GetComponent<PlayerHealth>();
        
        // Set the target location to the player's position and calculate the distance to them
        targetlocation = player.transform.position;
        distance = Vector3.Distance(transform.position, targetlocation);
        
        // Set the speed based on the distance and initial speed
        // It scales so the grenade will always take roughly the same amount
            // time to reach the player
        speed = distance * initialSpeed;
        
        // Calculate the scaling factor for size adjustments
        scalingFactor = 1 + speed * multiplier;
    }



    // Updates the grenade's movement and behavior over time
    private void FixedUpdate()
    {
        // Increment the timer
        curTime += Time.deltaTime;
        
        // Move the grenade towards the player's position
        transform.position = Vector3.MoveTowards(transform.position, targetlocation, speed * Time.deltaTime);
        
        // Calculate the current distance to the target and the player
        currentDistance = Vector3.Distance(transform.position, targetlocation);
        playerDistance = Vector3.Distance(transform.position, player.transform.position);

        // Increases the scale of the grenade during the first 25% of its path
        if (currentDistance > distance / 4)
        {
            // Increase scale gradually
            float scaleIncrease = 1 + scalingFactor * Time.deltaTime;
            transform.localScale *= scaleIncrease;
        
            // Limit the scale to the maximum size
            if (transform.localScale.x >= max)
            {
                transform.localScale = Vector3.one * max;
            }
        }
        // Decreases the scale during the last 25% of its path
        else if (currentDistance < distance - distance / 4)
        {
            // Decrease scale gradually
            float scaleDecrease = 1 - scalingFactor * Time.deltaTime;
            transform.localScale *= scaleDecrease;
        
            // Limit the scale to the minimum size
            if (transform.localScale.x <= min)
            {
                transform.localScale = Vector3.one * min;
            }
        }
        
        // Trigger explosion if the grenade has reached its target
        if(currentDistance <= 0)
        {
            explode();
        }
    }



    // Handles the grenade's explosion logic
    void explode()
    {
        // Perform a circular cast to detect any objects within the explosion range
        RaycastHit2D hit = Physics2D.CircleCast(transform.position, explosionRange, targetlocation, explosionRange);
        
        // Check if we hit anything
        if (hit != false)
        {
            Debug.Log("Something was hit!");
            
            // If the player is hit, calculate damage based on distance
            if (hit.collider.tag == "Player")
            {
                Debug.Log("Player was in range!");
                
                // Calculate grenade damage inversely proportional to distance
                grenadeDamage = baseDamage / playerDistance;
                
                // If damage is too low, no effect
                // This is to prevent annoying tick damage
                if(grenadeDamage > 5)
                {
                    Debug.Log("Player took some damage!");
                    playerHealth.TakeDamage(grenadeDamage);
                }
            }

            // Check if any enemies are hit and apply damage
            if (hit.collider.tag == "Apple" || hit.collider.tag == "Lemon" || hit.collider.tag == "Orange" || hit.collider.tag == "Grape")
            {
                Debug.Log("Uh oh! Friendly took damage!");
                
                // Calculate damage based on distance to enemy
                float enemypos = Vector3.Distance(transform.position, hit.transform.position);
                grenadeDamage = baseDamage / enemypos;
                
                // Apply damage to the enemy
                // We don't care if they annoying tick damage or not
                hit.collider.GetComponent<EnemyHealth>().TakeDamage(grenadeDamage);
            }
        }

        // Destroy the grenade
        Destroy(gameObject);
    }
}
