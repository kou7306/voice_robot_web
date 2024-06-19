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

// テキストを作成
const loader = new THREE.FontLoader();
loader.load(
  "https://cdn.jsdelivr.net/npm/three@0.132.2/examples/fonts/helvetiker_regular.typeface.json",
  function (font) {
    const textGeometry = new THREE.TextGeometry("Congratulations!", {
      font: font,
      size: 50,
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

    const textMaterial = new THREE.MeshBasicMaterial({ color: 0x0000ff });
    const textMesh = new THREE.Mesh(textGeometry, textMaterial);
    textMesh.position.set(-textWidth / 2, -textHeight / 2, -100); // 画面の中央に配置
    textMesh.renderOrder = 1; // 手前に出す
    scene.add(textMesh);

    // 立方体をたくさん作成してランダムな位置に配置
    const cubeGeometry = new THREE.BoxGeometry(20, 20, 20);
    const cubeMaterials = [
      new THREE.MeshBasicMaterial({ color: 0xff0000 }),
      new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
      new THREE.MeshBasicMaterial({ color: 0x0000ff }),
      new THREE.MeshBasicMaterial({ color: 0xffff00 }),
      new THREE.MeshBasicMaterial({ color: 0xff00ff }),
      new THREE.MeshBasicMaterial({ color: 0x00ffff }),
    ];
    for (let i = 0; i < 100; i++) {
      const cube = new THREE.Mesh(cubeGeometry, cubeMaterials);
      cube.position.set(
        Math.random() * 600 - 300,
        Math.random() * 600 - 300,
        Math.random() * 600 - 300 - 200 // テキストよりも後ろに配置
      );
      scene.add(cube);
    }
  }
);

// カメラ位置を設定
camera.position.z = 300;

// アニメーションループ
function animate() {
  requestAnimationFrame(animate);

  // 立方体を下に向かって移動させる
  scene.traverse((object) => {
    if (object instanceof THREE.Mesh) {
      object.position.y -= 1;
      if (object.position.y < -300) {
        object.position.y = 300;
      }
    }
  });

  renderer.render(scene, camera);
}
animate();
