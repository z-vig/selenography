
# # Dependencies
# import numpy as np
# import cv2


# def surf(src, dst):
#     src = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
#     dst = cv2.imread(dst, cv2.IMREAD_GRAYSCALE)

#     src = np.flip(src, axis=(0, 1))
#     # dst = np.flip(dst, axis=(0, 1))  # flipping horizontally and vertically

#     # fig, ax = plt.subplots(1, 2)
#     # for i in ax:
#     #     i.set_axis_off()

#     # ax[0].imshow(src)
#     # ax[1].imshow(dst)

#     feats = cv2.ORB_create()
#     kp1, dsc1 = feats.detectAndCompute(src, None)
#     kp2, dsc2 = feats.detectAndCompute(dst, None)

#     matcher = cv2.BFMatcher(normType=cv2.NORM_HAMMING)
#     matches = matcher.match(dsc1, dsc2)
#     matches = sorted(matches, key=lambda x: x.distance)[:]

#     good_matches = []
#     for m in matches:
#         from_pt = kp1[m.queryIdx].pt
#         to_pt = kp2[m.trainIdx].pt

#         dist = abs(from_pt[1] - to_pt[1])
#         if dist < 30:
#             good_matches.append(m)

#     match_image = cv2.drawMatches(src, kp1, dst, kp2, good_matches, None)
#     match_image = cv2.resize(match_image, (1000, 650))

#     homo_pts1 = np.zeros((len(good_matches), 2), dtype='float')
#     homo_pts2 = np.zeros((len(good_matches), 2), dtype='float')

#     for n, m in enumerate(good_matches):
#         homo_pts1[n] = kp1[m.queryIdx].pt
#         homo_pts2[n] = kp2[m.trainIdx].pt

#     H, mask = cv2.findHomography(homo_pts1, homo_pts2, method=cv2.RANSAC)

#     h, w = src.shape
#     aligned = cv2.warpPerspective(dst, H, (w, h))

#     fig, ax = plt.subplots(1, 2)
#     ax[0].imshow(aligned, cmap="Grays_r")
#     ax[1].imshow(src, cmap="Grays_r")
#     for i in ax:
#         i.set_axis_off()
#     # fig, ax = plt.subplots(1, 2)
#     # ax[0].imshow(img_with_kp1)
#     # ax[1].imshow(img_with_kp2)
#     # ax[0].set_axis_off()
#     # ax[1].set_axis_off()

#     cv2.imshow("Matches", match_image)
#     cv2.waitKey(1000)
