import { FilesetResolver, GestureRecognizer } from "@mediapipe/tasks-vision";

export class MediaPipeService {
  private static recognizer: GestureRecognizer | null = null;
  private static initPromise: Promise<GestureRecognizer> | null = null;

  static async initialize() {
    if (this.recognizer) return this.recognizer;
    if (this.initPromise) return this.initPromise;

    console.log("Initializing MediaPipe Vision...");

    this.initPromise = (async () => {
      try {
        let vision;
        // Use local assets from public/models
        console.log("Loading MediaPipe WASM from local assets...");
        vision = await FilesetResolver.forVisionTasks(
          "/models"
        );

        const recognizer = await GestureRecognizer.createFromOptions(vision, {
          baseOptions: {
            modelAssetPath: "/models/gesture_recognizer.task",
            delegate: "GPU"
          },
          runningMode: "VIDEO",
          numHands: 2,
        });

        console.log("MediaPipe Initialized Successfully");
        this.recognizer = recognizer;
        return recognizer;
      } catch (error) {
        console.error("Failed to initialize MediaPipe:", error);
        this.initPromise = null; // Reset promise on failure to allow retry
        throw error;
      }
    })();

    return this.initPromise;
  }
}