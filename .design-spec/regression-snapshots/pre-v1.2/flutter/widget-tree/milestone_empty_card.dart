import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/theme/capped_text_theme.dart';
import '../../../../core/widgets/widgets.dart';
import '../../../../router/app_routes.dart';
import '../../../coupons/presentation/providers/wishlist_providers.dart';

/// Empty state da `MilestoneTrack` quando wishlist=0. Atalho de descoberta
/// pra Léo iniciante: comunica que existe shop + mostra cap visual (`0/$cap`)
/// + sugere o flow ("marca", "pega quando der saldo"). Substituído pela
/// barra cheia no instante em que o user marca o primeiro cupom como Querer.
class MilestoneEmptyCard extends ConsumerWidget {
  const MilestoneEmptyCard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final colors = context.colors;
    final capped = context.cappedTextTheme;
    final textTheme = Theme.of(context).textTheme;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cap = ref.watch(wishlistCapProvider);
    final chevronColor = isDark ? colors.brandPressed : colors.brandDefault;

    return Padding(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.xl,
        vertical: AppSpacing.sm,
      ),
      child: AppCard(
        padding: const EdgeInsets.all(AppSpacing.lg),
        onTap: () => context.pushNamed(AppRoutes.cupomShop),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'CUPONS QUE VOCÊ QUER · 0/$cap',
                    style: capped.labelSmall?.copyWith(
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      letterSpacing: 1.2,
                      color: colors.textSecondary,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    'Marca o que você quer no shop.',
                    style: textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                      letterSpacing: -0.2,
                      color: colors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    'Pega quando der saldo.',
                    style: textTheme.bodySmall?.copyWith(
                      fontWeight: FontWeight.w500,
                      color: colors.textSecondary,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: AppSpacing.lg),
            const _GhostStack(),
            const SizedBox(width: AppSpacing.xs),
            Icon(
              Icons.chevron_right_rounded,
              size: 18,
              color: chevronColor,
            ),
          ],
        ),
      ),
    );
  }
}

/// Pilha de 3 anéis pontilhados que evocam os `MilestoneNode` da barra
/// cheia (anel 46px), reduzidos a 30px e sobrepostos -8px. Promessa visual
/// do que estaria ali quando o user marcar o primeiro cupom.
class _GhostStack extends StatelessWidget {
  const _GhostStack();

  static const double _ringSize = 30;
  static const double _overlap = 8;
  static const int _count = 3;

  @override
  Widget build(BuildContext context) {
    final colors = context.colors;
    final ringColor = colors.textPrimary.withValues(alpha: 0.14);
    const width = _ringSize + (_ringSize - _overlap) * (_count - 1);
    return SizedBox(
      width: width,
      height: _ringSize,
      child: Stack(
        children: [
          for (var i = 0; i < _count; i++)
            Positioned(
              left: (_ringSize - _overlap) * i,
              top: 0,
              child: SizedBox(
                width: _ringSize,
                height: _ringSize,
                child: CustomPaint(
                  painter: _DashedRingPainter(color: ringColor),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

class _DashedRingPainter extends CustomPainter {
  _DashedRingPainter({required this.color});

  final Color color;

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final radius = size.width / 2 - 1;
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5;
    const segments = 14;
    const dashFraction = 0.55;
    const segArc = (2 * math.pi) / segments;
    for (var i = 0; i < segments; i++) {
      final start = i * segArc;
      canvas.drawArc(
        Rect.fromCircle(center: center, radius: radius),
        start,
        segArc * dashFraction,
        false,
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant _DashedRingPainter old) => old.color != color;
}
