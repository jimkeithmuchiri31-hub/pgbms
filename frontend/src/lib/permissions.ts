export const ROLE_MODULE_ACCESS: Record<string, string[]> = {
  SUPER_ADMIN: ["members", "attendance", "training", "finance", "welfare", "inventory", "meetings", "documents", "reports"],
  ADMIN: ["members", "attendance", "training", "finance", "welfare", "inventory", "meetings", "documents", "reports"],
  OFFICER: ["members", "attendance", "training", "meetings"],
  TREASURER: ["finance", "reports"],
  TRAINING_OFFICER: ["training", "attendance"],
  SECRETARY: ["documents", "meetings", "members"],
  VIEWER: ["reports"],
};

export function canAccessModule(role: string | undefined, module: string): boolean {
  if (!role) return false;
  if (role === "SUPER_ADMIN") return true;
  return ROLE_MODULE_ACCESS[role]?.includes(module) ?? false;
}