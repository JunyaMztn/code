import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def compute_cov_and_corr_images(raw, pattern, win_size=5, stride=1, output='cov'):
    """
    モザイクRAW画像から、色成分間の共分散または相関係数画像を生成。

    output: 'cov'（共分散） or 'corr'（相関係数）
    """
    H, W = raw.shape
    ph, pw = pattern.shape

    # マスク作成
    masks = {c: np.zeros((ph, pw), bool) for c in ['R','G','B','IR']}
    for i in range(ph):
        for j in range(pw):
            masks[pattern[i, j]][i, j] = True

    # 色プレーン生成
    planes = {}
    for c, mask in masks.items():
        tile_mask = np.tile(mask, (H//ph+1, W//pw+1))[:H, :W]
        planes[c] = raw * tile_mask

    # パッチ抽出
    pad = win_size//2
    sw = lambda x: sliding_window_view(np.pad(x, pad), (win_size, win_size))[::stride, ::stride]
    patches = np.stack([sw(planes[c]) for c in ['R','G','B','IR']], axis=-1)
    h, w, _, _, _ = patches.shape

    # 有効画素マスクとカウント
    valid = patches.sum(axis=(2,3)) != 0
    counts = valid.sum(axis=-1)
    good = counts >= 4
    counts = np.maximum(counts, 1)

    # セントライズ
    sums = patches.sum(axis=(2,3))
    means = sums / counts[..., None]
    centered = patches - means[:, :, None, None, :]

    # 共分散計算
    covs = np.einsum('hwijc,hwijd->hwijcd', centered, centered) / (counts[..., None, None] - 1)
    covs[~good, ...] = 0

    # 出力モードによる処理
    channels = ['R','G','B','IR']
    output_imgs = {}
    if output == 'cov':
        for i in range(4):
            for j in range(i+1, 4):
                output_imgs[(channels[i], channels[j])] = covs[:, :, i, j]
    else:  # 'corr'
        var = np.diagonal(covs, axis1=2, axis2=3)  # shape (h,w,4)
        sigma = np.sqrt(var)
        outer = sigma[..., :, None] * sigma[..., None, :]
        corr = covs / (outer + 1e-8)
        corr[outer == 0] = 0
        for i in range(4):
            for j in range(i+1, 4):
                output_imgs[(channels[i], channels[j])] = corr[:, :, i, j]

    return output_imgs

# ======= 使用例 =======
pattern = np.array([
    ['R','G','B','G'],
    ['G','IR','G','IR'],
    ['B','G','R','G'],
    ['G','IR','G','IR'],
])
np.random.seed(0)
raw = np.random.randint(0,256,(16,16)).astype(float)

# 共分散画像
cov_imgs = compute_cov_and_corr_images(raw, pattern, win_size=5, stride=1, output='cov')
# 相関係数画像
corr_imgs = compute_cov_and_corr_images(raw, pattern, win_size=5, stride=1, output='corr')

print("cov RG:", cov_imgs[('R','G')].shape, "corr RG:", corr_imgs[('R','G')].shape)
