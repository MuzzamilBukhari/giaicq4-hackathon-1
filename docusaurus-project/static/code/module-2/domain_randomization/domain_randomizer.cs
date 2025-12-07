using UnityEngine;
using System.Collections.Generic;

public class DomainRandomizer : MonoBehaviour
{
    public List<Renderer> renderersToRandomize;
    public Color[] baseColors = { Color.red, Color.green, Color.blue, Color.yellow, Color.magenta };
    public float minBrightness = 0.3f;
    public float maxBrightness = 0.9f;
    public float textureScaleMin = 0.5f;
    public float textureScaleMax = 2.0f;

    void Start()
    {
        RandomizeEnvironment();
    }

    public void RandomizeEnvironment()
    {
        foreach (Renderer renderer in renderersToRandomize)
        {
            // Randomize color
            Color randomColor = baseColors[Random.Range(0, baseColors.Length)];
            float brightness = Random.Range(minBrightness, maxBrightness);
            Color finalColor = new Color(
                randomColor.r * brightness,
                randomColor.g * brightness,
                randomColor.b * brightness
            );
            renderer.material.color = finalColor;

            // Randomize texture scale
            float scale = Random.Range(textureScaleMin, textureScaleMax);
            renderer.material.mainTextureScale = new Vector3(scale, scale, scale);

            // Randomize other material properties
            renderer.material.SetFloat("_Metallic", Random.Range(0f, 1f));
            renderer.material.SetFloat("_Smoothness", Random.Range(0f, 1f));
        }
    }

    void Update()
    {
        // Optional: Randomize periodically during simulation
        if (Random.value < 0.01f) // Randomize with 1% probability per frame
        {
            RandomizeEnvironment();
        }
    }
}