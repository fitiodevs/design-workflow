import 'dart:math' as math;

import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/theme/capped_text_theme.dart';

enum NodeState { done, progress, locked }

class MilestoneNode extends StatelessWidget {
  const MilestoneNode({
    super.key,
    required this.title,
    required this.imageUrl,
    required this.progress,
    required this.state,
    this.subtitle,
    required this.onTap,
  });

  final String title;
  final String imageUrl;

  /// Progresso 0..1. Ignorado quando `state == NodeState.done` (renderiza
  /// preenchido) ou `NodeState.locked` (renderiza traço pontilhado).
  final double progress;
  final NodeState state;
  final String? subtitle;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final colors = context.colors;
    final capped = context.cappedTextTheme;

    final ring = SizedBox(
      width: 46,
      height: 46,
      child: CustomPaint(
        painter: _ProgressRingPainter(
          progress: state == NodeState.done ? 1.0 : progress,
          state: state,
          filledColor: state == NodeState.done
              ? colors.feedbackSuccess
              : colors.gameAccent,
          trackColor: colors.textPrimary.withValues(alpha: 0.10),
        ),
        child: Center(child: _nodeIcon(context)),
      ),
    );

    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: onTap,
      child: SizedBox(
        width: 78,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ring,
            const SizedBox(height: AppSpacing.sm),
            Text(
              title,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
              style: capped.labelSmall?.copyWith(
                fontSize: 10.5,
                fontWeight: FontWeight.w700,
                color: state == NodeState.locked
                    ? colors.textMuted
                    : colors.textPrimary,
                height: 1.2,
              ),
            ),
            if (subtitle != null) ...[
              const SizedBox(height: 2),
              Text(
                subtitle!,
                style: capped.labelSmall?.copyWith(
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                  color: colors.textMuted,
                  letterSpacing: 0.4,
                  height: 1.2,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _nodeIcon(BuildContext context) {
    final colors = context.colors;
    if (state == NodeState.done) {
      return const Icon(Icons.check_rounded, size: 22, color: Colors.white);
    }
    if (imageUrl.isNotEmpty) {
      return ClipOval(
        child: SizedBox(
          width: 32,
          height: 32,
          child: CachedNetworkImage(
            imageUrl: imageUrl,
            fit: BoxFit.cover,
            fadeInDuration: Duration.zero,
            placeholder: (context, url) => Container(color: colors.bgBase),
            errorWidget: (context, url, error) => Icon(
              Icons.local_offer_outlined,
              size: 18,
              color: state == NodeState.locked
                  ? colors.textMuted
                  : colors.gameAccentOnColor,
            ),
          ),
        ),
      );
    }
    return Icon(
      Icons.local_offer_outlined,
      size: 20,
      color: state == NodeState.locked
          ? colors.textMuted.withValues(alpha: 0.45)
          : colors.gameAccentOnColor,
    );
  }
}

class _ProgressRingPainter extends CustomPainter {
  _ProgressRingPainter({
    required this.progress,
    required this.state,
    required this.filledColor,
    required this.trackColor,
  });

  final double progress;
  final NodeState state;
  final Color filledColor;
  final Color trackColor;

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final radius = size.width / 2 - 1.5;

    if (state == NodeState.done) {
      final fill = Paint()
        ..color = filledColor
        ..style = PaintingStyle.fill;
      canvas.drawCircle(center, radius, fill);
      return;
    }

    if (state == NodeState.locked) {
      _drawDashedCircle(canvas, center, radius, trackColor);
      return;
    }

    final track = Paint()
      ..color = trackColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;
    canvas.drawCircle(center, radius, track);

    if (progress > 0) {
      final filled = Paint()
        ..color = filledColor
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3
        ..strokeCap = StrokeCap.round;
      final sweep = 2 * math.pi * progress;
      canvas.drawArc(
        Rect.fromCircle(center: center, radius: radius),
        -math.pi / 2,
        sweep,
        false,
        filled,
      );
    }
  }

  void _drawDashedCircle(Canvas canvas, Offset center, double r, Color color) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;
    const segments = 16;
    const dashFraction = 0.6;
    const segArc = (2 * math.pi) / segments;
    for (var i = 0; i < segments; i++) {
      final start = i * segArc;
      canvas.drawArc(
        Rect.fromCircle(center: center, radius: r),
        start,
        segArc * dashFraction,
        false,
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant _ProgressRingPainter old) =>
      old.progress != progress ||
      old.state != state ||
      old.filledColor != filledColor;
}
