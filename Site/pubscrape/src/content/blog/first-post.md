---
title: ' Estimating Control Barriers from Offline Data '
description: 'Learning-based methods for constructing control barrier functions (CBFs) are gaining popularity for ensuring safe robot control. '
pubDate: '21 Feb 2025'
heroImage: '/blog-placeholder-3.jpg'
---

 A major limitation of existing methods is their reliance on extensive sampling over the state space or online system interaction in simulation. In this work we propose a novel framework for learning neural CBFs through a fixed, sparsely-labeled dataset collected prior to training. Our approach introduces new annotation techniques based on out-of-distribution analysis, enabling efficient knowledge propagation from the limited labeled data to the unlabeled data. We also eliminate the dependency on a high-performance expert controller, and allow multiple sub-optimal policies or even manual control during data collection. We evaluate the proposed method on real-world platforms. With limited amount of offline data, it achieves state-of-the-art performance for dynamic obstacle avoidance, demonstrating statistically safer and less conservative maneuvers compared to existing methods. 

 Paper at: https://arxiv.org/pdf/2503.10641