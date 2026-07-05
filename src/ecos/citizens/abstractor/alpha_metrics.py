class AlphaMetrics:
    def compute_alpha(self, validation) -> float:
        """Calcule α ∈ [0,1] : plus proche de 1, plus l'abstraction est pure."""
        weights = [0.3, 0.2, 0.2, 0.2, 0.1]  # L0 le plus important
        scores = [
            float(validation.l0_present),
            float(validation.l1_dag_valid),
            float(validation.l2_protocol_valid),
            float(validation.l3_structure_valid),
            float(validation.l4_implementation_valid)
        ]
        alpha = sum(w * s for w, s in zip(weights, scores))
        # Pénalité forte si L0 absent
        if not validation.l0_present:
            alpha *= 0.5
        return round(alpha, 3)
