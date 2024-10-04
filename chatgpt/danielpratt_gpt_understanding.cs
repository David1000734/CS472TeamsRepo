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

        if (currentDistance > distance / 4)
        {
            transform.localScale = new Vector3(transform.localScale.x + transform.localScale.x * scalingFactor * Time.deltaTime, transform.localScale.y + transform.localScale.y * scalingFactor * Time.deltaTime, transform.localScale.z + transform.localScale.z * scalingFactor * Time.deltaTime);
            if (transform.localScale.x >= max && transform.localScale.y >= max)
            {
                transform.localScale = new Vector3(max, max, max);
            }
        } else if (currentDistance < distance - distance / 4)
        {
            transform.localScale = new Vector3(transform.localScale.x + transform.localScale.x * scalingFactor * Time.deltaTime * -1, transform.localScale.y + transform.localScale.y * scalingFactor * Time.deltaTime * -1, transform.localScale.z + transform.localScale.z * scalingFactor * Time.deltaTime * -1);
            if (transform.localScale.x <= min && transform.localScale.y <= min)
            {
                transform.localScale = new Vector3(min, min, min);
            }
        } else
        {
            transform.localScale = new Vector3(transform.localScale.x, transform.localScale.y, transform.localScale.z);
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
