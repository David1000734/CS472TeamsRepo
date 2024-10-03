using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LemonGrenade : MonoBehaviour
{
    PlayerHealth playerHealth;
    GameObject player;

    public float distance;
    public float currentDistance;

    public float multiplier;
    public float initialSpeed;

    public float max;
    public float min;

    public float curTime;
    public float scalingFactor;

    public float baseDamage;
    public float speed;

    private Vector3 targetlocation;
    private float grenadeDamage;

    private float playerDistance;
    public float explosionRange;

    private void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player");
        playerHealth = player.GetComponent<PlayerHealth>();
        targetlocation = player.transform.position;
        distance = Vector3.Distance(transform.position, targetlocation);
        speed = distance * initialSpeed;
        scalingFactor = 1 + speed * multiplier;
    }

    private void FixedUpdate()
    {
        curTime += Time.deltaTime;
        transform.position = Vector3.MoveTowards(transform.position, targetlocation, speed * Time.deltaTime);
        currentDistance = Vector3.Distance(transform.position, targetlocation);
        playerDistance = Vector3.Distance(transform.position, player.transform.position);

        // Increases the scale of the object at a continuous rate to a certain maximum for the first 25% of the path.

        // Calculate the scaling factor based on currentDistance
        if (currentDistance > distance / 4)
        {
            float scaleIncrease = 1 + scalingFactor * Time.deltaTime;
            transform.localScale *= scaleIncrease;
        
            // Clamp the scale to the maximum
            if (transform.localScale.x >= max)
            {
                transform.localScale = Vector3.one * max;
            }
        }

        // Decreases the scale of the object at a continuous rate to a certain minimum for the last 25% of the path.
        
        else if (currentDistance < distance - distance / 4)
        {
            float scaleDecrease = 1 - scalingFactor * Time.deltaTime;
            transform.localScale *= scaleDecrease;
        
            // Clamp the scale to the minimum
            if (transform.localScale.x <= min)
            {
                transform.localScale = Vector3.one * min;
            }
        }
        if(currentDistance <= 0)
        {
            explode();
        }
    }

    void explode()
    {
        Debug.Log("Throw");
        RaycastHit2D hit = Physics2D.CircleCast(transform.position, explosionRange, targetlocation, explosionRange);
        if (hit != false)
        {
            Debug.Log("Hit");
            if (hit.collider.tag == "Player")
            {
                Debug.Log("Player");
                grenadeDamage = baseDamage / playerDistance;
                if(grenadeDamage <= 5)
                {
                    Debug.Log("NoDMG");
                    Destroy(gameObject);
                }
                if(grenadeDamage > 5)
                {
                    Debug.Log("Hurt");
                    playerHealth.TakeDamage(grenadeDamage);
                    Destroy(gameObject);
                }
            }
            if (hit.collider.tag == "Apple" || hit.collider.tag == "Lemon" || hit.collider.tag == "Orange" || hit.collider.tag == "Grape")
            {
                Debug.Log("Enemy");
                float enemypos = Vector3.Distance(transform.position, hit.transform.position);
                grenadeDamage = baseDamage / enemypos;
                hit.collider.GetComponent<EnemyHealth>().TakeDamage(grenadeDamage);
            }
        }
        if(hit == false)
        {
            Debug.Log("Miss");
            Destroy(gameObject);
        }
    }
}
