export interface PlatformConfig {
  name: string;
  nameEn: string;
  color: string;
  baseUrl: string;
}

export type PlatformKey =
  | "tunwalai"
  | "readawrite"
  | "dekd"
  | "fictionlog"
  | "ookbee"
  | "meb";

export const PLATFORMS: Record<PlatformKey, PlatformConfig> = {
  tunwalai: {
    name: "ธันวลัย",
    nameEn: "Tunwalai",
    color: "#FF1744", // สีแดง
    baseUrl: "https://www.tunwalai.com",
  },
  readawrite: {
    name: "ReadAWrite",
    nameEn: "ReadAWrite",
    color: "#2962FF", // สีน้ำเงิน
    baseUrl: "https://www.readawrite.com",
  },
  dekd: {
    name: "Dek-D",
    nameEn: "Dek-D",
    color: "#00C853", // สีเขียว
    baseUrl: "https://www.dek-d.com",
  },
  fictionlog: {
    name: "Fictionlog",
    nameEn: "Fictionlog",
    color: "#9C27B0", // สีม่วง
    baseUrl: "https://www.fictionlog.co",
  },
  ookbee: {
    name: "Ookbee",
    nameEn: "Ookbee",
    color: "#FF6F00", // สีส้ม
    baseUrl: "https://www.ookbee.com",
  },
  meb: {
    name: "Meb",
    nameEn: "Meb",
    color: "#1565C0", // สีน้ำเงินเข้ม
    baseUrl: "https://www.meb.co.th",
  },
};

// Helper function to get platform config by key
export function getPlatformConfig(key: string): PlatformConfig | null {
  return PLATFORMS[key as PlatformKey] || null;
}

// Helper function to get all platform keys
export function getAllPlatformKeys(): PlatformKey[] {
  return Object.keys(PLATFORMS) as PlatformKey[];
}
