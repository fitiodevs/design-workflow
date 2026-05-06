import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/theme/capped_text_theme.dart';
import '../../../../router/app_routes.dart';
import '../../../coupons/domain/entities/coupon.dart';
import '../../../coupons/domain/entities/coupon_extensions.dart';
import '../../../coupons/presentation/providers/wishlist_providers.dart';
import '../../../profile/presentation/providers/user_points_provider.dart';
import '../providers/feed_strings.dart';
import 'milestone_empty_card.dart';

/// Trilha horizontal de cupons "Querer" (modelo cupom-mechanics-v2 §1.1,
/// design Clara v4 Figma-anchored). Domínio FIXO 0–25.000 pts; densidade
/// 80px/1000pts → canvas físico 2030px (sempre scrollable em viewport
/// ~360px). Empty (zero wishlist) → `MilestoneEmptyCard`.
class MilestoneTrack extends ConsumerWidget {
  const MilestoneTrack({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final coupons = ref.watch(wishlistedCouponsProvider).value ?? const [];
    final saldo = ref.watch(userPointsProvider).value ?? 0;
    if (coupons.isEmpty) return const MilestoneEmptyCard();
    return _MilestoneTrackFilled(coupons: coupons, saldo: saldo);
  }
}

// === Constantes de geometria ===
const int _domainMax = 25000;
const double _scaleFactor = 0.080; // 80px / 1000pts
const double _canvasReserve = 15; // half thumb-size, edge padding
const double _canvasUsable = _domainMax * _scaleFactor; // 2000
const double _canvasWidth = _canvasUsable + _canvasReserve * 2; // 2030

const double _barHeight = 15;
const double _barCenterY = 30; // vertical centerline within stack
const double _thumbSize = 30; // thumb extrapola ~14px acima/abaixo da bar (15)
const double _marcoSize = 11; // < bar (15) — marco respira dentro da barra
const double _stackHeight = 100; // bar + half-thumb above/below (44) + label + folga
const double _minThumbSpacing = 30; // 1 thumb-width
const double _stackOffset = 18; // half-thumb + small gap

const List<int> _marcoValues = [1000, 5000, 10000, 20000, 25000];

class _MilestoneTrackFilled extends StatelessWidget {
  const _MilestoneTrackFilled({required this.coupons, required this.saldo});

  final List<Coupon> coupons;
  final int saldo;

  @override
  Widget build(BuildContext context) {
    final colors = context.colors;
    final capped = context.cappedTextTheme;
    final textTheme = Theme.of(context).textTheme;
    final saldoX = (saldo * _scaleFactor).clamp(0.0, _canvasUsable);

    return Padding(
      padding: const EdgeInsets.fromLTRB(
        0,
        AppSpacing.md,
        0,
        AppSpacing.md,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xl),
            child: _Header(
              count: coupons.length,
              colors: colors,
              capped: capped,
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          _ScrollableTrack(
            coupons: coupons,
            saldoX: saldoX,
            colors: colors,
            textTheme: textTheme,
          ),
        ],
      ),
    );
  }
}

class _Header extends StatelessWidget {
  const _Header({
    required this.count,
    required this.colors,
    required this.capped,
  });

  final int count;
  final AppColors colors;
  final TextTheme capped;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          '${FeedStrings.milestoneSectionLabel.toUpperCase()} · $count',
          style: capped.labelSmall?.copyWith(
            fontSize: 11,
            fontWeight: FontWeight.w700,
            letterSpacing: 1.2,
            color: colors.textSecondary,
          ),
        ),
        GestureDetector(
          behavior: HitTestBehavior.opaque,
          onTap: () => context.pushNamed(AppRoutes.cupomShop),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                FeedStrings.milestoneSeeAll,
                style: capped.labelSmall?.copyWith(
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                  color: colors.brandDefault,
                ),
              ),
              Icon(
                Icons.chevron_right_rounded,
                size: 14,
                color: colors.brandDefault,
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _ScrollableTrack extends StatelessWidget {
  const _ScrollableTrack({
    required this.coupons,
    required this.saldoX,
    required this.colors,
    required this.textTheme,
  });

  final List<Coupon> coupons;
  final double saldoX;
  final AppColors colors;
  final TextTheme textTheme;

  @override
  Widget build(BuildContext context) {
    final positions = _computePositions(coupons);
    return SizedBox(
      height: _stackHeight,
      child: ShaderMask(
        shaderCallback: (rect) => const LinearGradient(
          stops: [0.0, 0.04, 0.96, 1.0],
          colors: [
            Color(0x00000000),
            Color(0xFF000000),
            Color(0xFF000000),
            Color(0x00000000),
          ],
        ).createShader(rect),
        blendMode: BlendMode.dstIn,
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          physics: const BouncingScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.xl),
          child: SizedBox(
            width: _canvasWidth,
            height: _stackHeight,
            child: _TrackCanvas(
              positions: positions,
              saldoX: saldoX,
              colors: colors,
              textTheme: textTheme,
            ),
          ),
        ),
      ),
    );
  }
}

class _TrackCanvas extends StatelessWidget {
  const _TrackCanvas({
    required this.positions,
    required this.saldoX,
    required this.colors,
    required this.textTheme,
  });

  final List<_PinPosition> positions;
  final double saldoX;
  final AppColors colors;
  final TextTheme textTheme;

  @override
  Widget build(BuildContext context) {
    // Render order: backs first (lower z), fronts last (top z)
    final ordered = [
      ...positions.where((p) => p.isBack),
      ...positions.where((p) => !p.isBack),
    ];
    return Stack(
      clipBehavior: Clip.none,
      children: [
        // bar bg
        Positioned(
          left: _canvasReserve,
          top: _barCenterY - _barHeight / 2,
          width: _canvasUsable,
          height: _barHeight,
          child: Container(
            decoration: BoxDecoration(
              color: colors.gameAccentMuted,
              borderRadius: BorderRadius.circular(AppRadius.pill),
            ),
          ),
        ),
        // bar fill
        if (saldoX > 0)
          Positioned(
            left: _canvasReserve,
            top: _barCenterY - _barHeight / 2,
            width: saldoX,
            height: _barHeight,
            child: Container(
              decoration: BoxDecoration(
                color: colors.gameAccent,
                borderRadius: BorderRadius.circular(AppRadius.pill),
              ),
            ),
          ),
        // start dot (0 mark, sem label) — clamp interno pra ficar dentro da barra
        _Marco(
          left: _clampMarcoLeft(_canvasReserve),
          label: null,
          colors: colors,
          textTheme: textTheme,
        ),
        // marcos — clamp idem (25k cairia em cima da borda direita sem isso)
        for (final value in _marcoValues)
          _Marco(
            left: _clampMarcoLeft(_canvasReserve + value * _scaleFactor),
            label: _formatMarco(value),
            colors: colors,
            textTheme: textTheme,
          ),
        // thumbs
        for (final pos in ordered)
          _Thumb(
            position: pos,
            colors: colors,
            onTap: () => context.push(AppPaths.cupomDetalhe(pos.coupon.uid)),
          ),
      ],
    );
  }
}

class _Marco extends StatelessWidget {
  const _Marco({
    required this.left,
    required this.label,
    required this.colors,
    required this.textTheme,
  });

  final double left;
  final String? label;
  final AppColors colors;
  final TextTheme textTheme;

  @override
  Widget build(BuildContext context) {
    const dotTop = _barCenterY - _marcoSize / 2;
    return Stack(
      clipBehavior: Clip.none,
      children: [
        Positioned(
          left: left - _marcoSize / 2,
          top: dotTop,
          width: _marcoSize,
          height: _marcoSize,
          child: Container(
            decoration: BoxDecoration(
              color: colors.borderStrong,
              shape: BoxShape.circle,
            ),
          ),
        ),
        if (label != null)
          Positioned(
            left: left - 32, // 64px wide label centered
            top: dotTop + _marcoSize + 6,
            width: 64,
            child: Text(
              label!,
              textAlign: TextAlign.center,
              style: textTheme.bodySmall?.copyWith(
                fontWeight: FontWeight.w400,
                color: colors.textPrimary,
              ),
            ),
          ),
      ],
    );
  }
}

class _Thumb extends StatelessWidget {
  const _Thumb({
    required this.position,
    required this.colors,
    required this.onTap,
  });

  final _PinPosition position;
  final AppColors colors;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final coupon = position.coupon;
    final fallback = coupon.title.isNotEmpty
        ? coupon.title.substring(0, 1).toUpperCase()
        : '?';
    return Positioned(
      left: position.left - _thumbSize / 2,
      top: _barCenterY - _thumbSize / 2,
      width: _thumbSize,
      height: _thumbSize,
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onTap,
        child: Container(
          decoration: BoxDecoration(
            color: colors.brandDefault,
            shape: BoxShape.circle,
            border: Border.all(color: colors.bgBase, width: 2),
          ),
          clipBehavior: Clip.antiAlias,
          child: coupon.imageUrl.isNotEmpty
              ? CachedNetworkImage(
                  imageUrl: coupon.imageUrl,
                  fit: BoxFit.cover,
                  fadeInDuration: Duration.zero,
                  placeholder: (_, _) =>
                      Container(color: colors.brandDefault),
                  errorWidget: (_, _, _) => _ThumbFallback(
                    letter: fallback,
                    colors: colors,
                  ),
                )
              : _ThumbFallback(letter: fallback, colors: colors),
        ),
      ),
    );
  }
}

class _ThumbFallback extends StatelessWidget {
  const _ThumbFallback({required this.letter, required this.colors});

  final String letter;
  final AppColors colors;

  @override
  Widget build(BuildContext context) {
    return Container(
      color: colors.brandDefault,
      alignment: Alignment.center,
      child: Text(
        letter,
        style: TextStyle(
          color: colors.textOnBrand,
          fontWeight: FontWeight.w800,
          fontSize: 12,
        ),
      ),
    );
  }
}

class _PinPosition {
  const _PinPosition({
    required this.coupon,
    required this.left,
    required this.isBack,
  });

  final Coupon coupon;
  final double left;
  final bool isBack;
}

/// Calcula posições físicas de cada cupom no canvas, resolvendo overlap
/// horizontal: quando 2+ cupons ficam a < 30px (1 thumb-width) entre si,
/// força distância mínima de 18px e marca o mais à direita como "back"
/// (opacity reduzida, z-index menor — efeito stack lateral).
List<_PinPosition> _computePositions(List<Coupon> coupons) {
  final sorted = [...coupons]
    ..sort((a, b) => a.pointsCost.compareTo(b.pointsCost));
  final positions = <_PinPosition>[];
  for (final coupon in sorted) {
    final natural = _canvasReserve + coupon.pointsCost * _scaleFactor;
    if (positions.isEmpty) {
      positions.add(_PinPosition(coupon: coupon, left: natural, isBack: false));
      continue;
    }
    final lastLeft = positions.last.left;
    if (natural - lastLeft < _minThumbSpacing) {
      positions.add(_PinPosition(
        coupon: coupon,
        left: lastLeft + _stackOffset,
        isBack: true,
      ));
    } else {
      positions.add(_PinPosition(coupon: coupon, left: natural, isBack: false));
    }
  }
  return positions;
}

/// Limita a posição central do marco a um inset interno calibrado visual-
/// mente (não geométrico): 0 ancora em 34, 25k ancora em 2024 — folga
/// suficiente pra ler como "dentro da barra" e não como "encostado na
/// borda". Marcos do meio (1k, 5k, 10k, 20k) passam intactos.
const double _marcoMinLeft = 23;
const double _marcoMaxLeft = 2007; // simétrico: canvas_reserve(15) + usable(2000) - 8

double _clampMarcoLeft(double natural) {
  if (natural < _marcoMinLeft) return _marcoMinLeft;
  if (natural > _marcoMaxLeft) return _marcoMaxLeft;
  return natural;
}

/// Format BR pleno (1000 → "1.000", 25000 → "25.000").
String _formatMarco(int value) {
  final str = value.toString();
  if (str.length <= 3) return str;
  return '${str.substring(0, str.length - 3)}.${str.substring(str.length - 3)}';
}
