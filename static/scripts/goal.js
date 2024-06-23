// Three.js 初期化
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
const renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById("animationCanvas"),
});
renderer.setSize(window.innerWidth, window.innerHeight);

// カラフルなテキストマテリアルを作成
function createGradientMaterial(colors) {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 256;
  const context = canvas.getContext("2d");

  const gradient = context.createLinearGradient(
    0,
    0,
    canvas.width,
    canvas.height
  );
  for (let i = 0; i < colors.length; i++) {
    gradient.addColorStop(i / (colors.length - 1), colors[i]);
  }

  context.fillStyle = gradient;
  context.fillRect(0, 0, canvas.width, canvas.height);

  const texture = new THREE.CanvasTexture(canvas);
  return new THREE.MeshBasicMaterial({ map: texture });
}

// テキストを作成
const loader = new THREE.FontLoader();
loader.load(
  "https://cdn.jsdelivr.net/npm/three@0.132.2/examples/fonts/helvetiker_regular.typeface.json",
  function (font) {
    const textGeometry = new THREE.TextGeometry("Congratulations!", {
      font: font,
      size: 70,
      height: 5,
      curveSegments: 12,
      bevelEnabled: true,
      bevelThickness: 2,
      bevelSize: 1,
      bevelSegments: 5,
    });
    textGeometry.computeBoundingBox(); // テキストの幅を計算
    const textWidth =
      textGeometry.boundingBox.max.x - textGeometry.boundingBox.min.x;
    const textHeight =
      textGeometry.boundingBox.max.y - textGeometry.boundingBox.min.y;

    const textMaterial = createGradientMaterial([
      "#ff0000",
      "#00ff00",
      "#0000ff",
    ]);
    const textMesh = new THREE.Mesh(textGeometry, textMaterial);
    textMesh.position.set(-textWidth / 2, -textHeight / 2, -100); // 画面の中央に配置
    textMesh.renderOrder = 1; // 手前に出す
    textMesh.name = "text"; // テキストメッシュに名前をつける
    scene.add(textMesh);

    // 球体をたくさん作成してランダムな位置に配置
    const sphereGeometry = new THREE.SphereGeometry(10, 32, 32);
    const sphereMaterials = [
      new THREE.MeshBasicMaterial({ color: 0xff0000 }),
      new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
      new THREE.MeshBasicMaterial({ color: 0x0000ff }),
      new THREE.MeshBasicMaterial({ color: 0xffff00 }),
      new THREE.MeshBasicMaterial({ color: 0xff00ff }),
      new THREE.MeshBasicMaterial({ color: 0x00ffff }),
    ];
    for (let i = 0; i < 100; i++) {
      const sphere = new THREE.Mesh(
        sphereGeometry,
        sphereMaterials[i % sphereMaterials.length]
      );
      sphere.position.set(
        Math.random() * 600 - 300,
        Math.random() * 600 - 300,
        Math.random() * 600 - 300 - 200 // テキストよりも後ろに配置
      );
      scene.add(sphere);
    }
  }
);

// カメラ位置を設定
camera.position.z = 300;

let time = 0;

// アニメーションループ
function animate() {
  requestAnimationFrame(animate);

  // 時間を更新
  time += 0.05;

  // テキストを振動させる
  const textMesh = scene.getObjectByName("text");
  if (textMesh) {
    textMesh.position.y = Math.sin(time) * 10; // 振動の幅を調整
  }

  // 球体を下に向かって移動させる
  scene.traverse((object) => {
    if (object instanceof THREE.Mesh && object.name !== "text") {
      object.position.y -= 1;
      if (object.position.y < -300) {
        object.position.y = 300;
      }
    }
  });

  renderer.render(scene, camera);
}
animate();
